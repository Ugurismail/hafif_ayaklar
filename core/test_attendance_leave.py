import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import AttendanceDayState
from core.views.attendance_views import ATTENDANCE_SLOTS, _get_sheet_config


class AttendanceLeaveRangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="attendance-admin",
            password="test-pass",
            is_staff=True,
        )
        self.client.force_login(self.user)
        self.config = _get_sheet_config()
        self.person = next(
            person
            for sheet in self.config.sheets
            for section in sheet["sections"]
            for person in section["people"]
            if person["name"] == "İsmail AYGÜN"
        )
        self.url = reverse("attendance_sheet_leave_range")

    def post_range(self, action="apply", start="2026-08-12", end="2026-08-15"):
        return self.client.post(
            self.url,
            data=json.dumps({
                "action": action,
                "person_id": self.person["id"],
                "start_date": start,
                "end_date": end,
            }),
            content_type="application/json",
        )

    def test_applies_leave_mark_to_every_slot_in_date_range(self):
        response = self.post_range()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["changed_days"], 4)
        states = AttendanceDayState.objects.order_by("date")
        self.assertEqual(states.count(), 4)
        for state in states:
            self.assertEqual(
                state.marks[self.person["id"]],
                {slot: "İ" for slot in ATTENDANCE_SLOTS},
            )

    def test_removing_range_only_removes_leave_marks(self):
        AttendanceDayState.objects.create(
            date="2026-08-12",
            marks={
                self.person["id"]: {
                    "morning-in": "İ",
                    "morning-out": "G",
                    "noon-in": "İ",
                },
            },
        )

        response = self.post_range(action="remove", start="2026-08-12", end="2026-08-12")

        self.assertEqual(response.status_code, 200)
        state = AttendanceDayState.objects.get(date="2026-08-12")
        self.assertEqual(state.marks[self.person["id"]], {"morning-out": "G"})

    def test_existing_daily_save_can_clear_automatic_leave(self):
        self.post_range(start="2026-08-12", end="2026-08-12")

        response = self.client.post(
            reverse("attendance_sheet_save"),
            data=json.dumps({
                "date": "2026-08-12",
                "sheets": self.config.sheets,
                "marks": {},
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(AttendanceDayState.objects.get(date="2026-08-12").marks, {})

    def test_rejects_reversed_date_range(self):
        response = self.post_range(start="2026-08-15", end="2026-08-12")

        self.assertEqual(response.status_code, 400)
        self.assertIn("Bitiş tarihi", response.json()["error"])
        self.assertFalse(AttendanceDayState.objects.exists())
