"""DJ-only printable personnel attendance sheet tool."""

import json
import re
from copy import deepcopy
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET, require_POST

from ..models import AttendanceDayState, AttendanceSheetConfig


ATTENDANCE_SLOTS = ("morning-in", "morning-out", "noon-in", "noon-out")
ATTENDANCE_MARKERS = {"İ", "G", "R", "H"}
PERSON_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,90}$")


DEFAULT_ATTENDANCE_SHEETS = [
    {
        "page": 1,
        "sections": [
            {"code": "120", "people": [
                "Hacı NALBANT",
                "Emrah YEŞİLBAŞ",
                "İsmail AYGÜN",
                "Mert Furkan TÖTÜNCÜ",
                "Said Mehdi DEMİR",
            ]},
            {"code": "130", "people": [
                "Ayşe ÖZCAN BATAN",
                "Makbule Aslı TANAGAR",
            ]},
            {"code": "140", "people": [
                "Mehmet BİRCAN",
                "Altuğ DEVECİOĞLU",
            ]},
            {"code": "145", "people": [
                "Elif ARI",
                "Çağla DOĞAN",
                "Akın KAYA",
            ]},
            {"code": "150", "people": [
                "Seval KILIÇ",
                "Hatice ASLAN",
            ]},
        ],
    },
    {
        "page": 2,
        "sections": [
            {"code": "160", "people": [
                "Dilek ÖZBAY",
                "Şevket Cansın BEYSANOĞLU",
            ]},
            {"code": "170", "people": [
                "Ezgi DİLMEN",
                "Dilek KOÇ",
                "Cahide Elif DİKAN",
            ]},
            {"code": "180", "people": [
                "D. Melih TÜRKOĞLU",
                "Sevgi TOPRAK AYDOĞDU",
            ]},
            {"code": "190", "people": [
                "Nazan AKYOL",
                "Meltem SÖZERİ",
            ]},
            {"code": "200", "people": [
                "Abdurrahman YILDIRIM",
                "Damla DEĞİRMENCİ",
                "Hülya OFLAZ",
            ]},
        ],
    },
]


def _user_can_use_attendance_tool(user):
    profile = getattr(user, "userprofile", None)
    return user.is_staff or getattr(profile, "is_dj", False)


def _require_attendance_permission(request):
    if not _user_can_use_attendance_tool(request.user):
        raise PermissionDenied


def _default_sheets():
    sheets = deepcopy(DEFAULT_ATTENDANCE_SHEETS)
    for sheet in sheets:
        for section in sheet["sections"]:
            section["people"] = [
                {
                    "id": f"p{sheet['page']}-{section['code']}-{index}",
                    "name": name,
                    "is_blank": False,
                }
                for index, name in enumerate(section["people"], start=1)
            ]
            if len(section["people"]) < 3:
                section["people"].append({
                    "id": f"blank-{sheet['page']}-{section['code']}-1",
                    "name": "",
                    "is_blank": True,
                })
    return sheets


def _normalize_person(raw_person, fallback_index):
    if isinstance(raw_person, str):
        name = raw_person.strip()
        person_id = f"legacy-{fallback_index}"
        is_blank = False
    elif isinstance(raw_person, dict):
        name = str(raw_person.get("name", "")).strip()
        person_id = str(raw_person.get("id", "")).strip()
        is_blank = bool(raw_person.get("is_blank")) or not name
    else:
        return None

    name = name[:90]
    if not PERSON_ID_PATTERN.match(person_id):
        person_id = f"person-{fallback_index}"

    return {"id": person_id, "name": name, "is_blank": is_blank}


def _normalize_sheets(raw_sheets):
    if not isinstance(raw_sheets, list):
        return _default_sheets()

    defaults = _default_sheets()
    posted_sections = {}
    for sheet in raw_sheets:
        if not isinstance(sheet, dict):
            continue
        page = sheet.get("page")
        for section in sheet.get("sections", []):
            if not isinstance(section, dict):
                continue
            code = str(section.get("code", "")).strip()
            posted_sections[f"{page}-{code}"] = section

    normalized = []
    fallback_index = 1
    seen_person_ids = set()

    for default_sheet in defaults:
        normalized_sheet = {"page": default_sheet["page"], "sections": []}
        for default_section in default_sheet["sections"]:
            section_key = f"{default_sheet['page']}-{default_section['code']}"
            posted_section = posted_sections.get(section_key, {})
            raw_people = posted_section.get("people", default_section["people"])
            if not isinstance(raw_people, list):
                raw_people = default_section["people"]

            people = []
            for raw_person in raw_people[:60]:
                person = _normalize_person(raw_person, fallback_index)
                fallback_index += 1
                if not person:
                    continue
                if person["id"] in seen_person_ids:
                    person["id"] = f"{person['id']}-{fallback_index}"
                seen_person_ids.add(person["id"])
                people.append(person)

            normalized_sheet["sections"].append({
                "code": default_section["code"],
                "people": people,
            })
        normalized.append(normalized_sheet)

    return normalized


def _get_sheet_config():
    defaults = _default_sheets()
    config, created = AttendanceSheetConfig.objects.get_or_create(
        key="default",
        defaults={"sheets": defaults},
    )
    if created:
        return config

    normalized = _normalize_sheets(config.sheets)
    if normalized != config.sheets:
        config.sheets = normalized
        config.save(update_fields=["sheets", "updated_at"])
    return config


def _valid_person_ids(sheets):
    return {
        person["id"]
        for sheet in sheets
        for section in sheet["sections"]
        for person in section["people"]
        if person["name"] and not person.get("is_blank")
    }


def _attendance_people(sheets):
    return [
        {
            "id": person["id"],
            "name": person["name"],
            "section": section["code"],
        }
        for sheet in sheets
        for section in sheet["sections"]
        for person in section["people"]
        if person["name"] and not person.get("is_blank")
    ]


def _normalize_marks(raw_marks, sheets):
    if not isinstance(raw_marks, dict):
        return {}

    valid_person_ids = _valid_person_ids(sheets)
    normalized = {}
    for person_id, raw_slots in raw_marks.items():
        person_id = str(person_id)
        if person_id not in valid_person_ids or not isinstance(raw_slots, dict):
            continue

        person_marks = {}
        for slot in ATTENDANCE_SLOTS:
            marker = str(raw_slots.get(slot, "")).strip()
            if marker in ATTENDANCE_MARKERS:
                person_marks[slot] = marker
        if person_marks:
            normalized[person_id] = person_marks

    return normalized


def _request_payload(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _date_from_value(value):
    parsed = parse_date(str(value or ""))
    return parsed or timezone.localdate()


@login_required
def attendance_sheet_tool(request):
    _require_attendance_permission(request)

    config = _get_sheet_config()
    today = timezone.localdate()
    day_state = AttendanceDayState.objects.filter(date=today).first()

    return render(request, "core/attendance_sheet_tool.html", {
        "sheets": config.sheets,
        "attendance_people": _attendance_people(config.sheets),
        "initial_date": today.isoformat(),
        "initial_marks": day_state.marks if day_state else {},
    })


@login_required
@require_GET
def attendance_day_state(request):
    _require_attendance_permission(request)

    config = _get_sheet_config()
    selected_date = _date_from_value(request.GET.get("date"))
    day_state = AttendanceDayState.objects.filter(date=selected_date).first()
    marks = _normalize_marks(day_state.marks, config.sheets) if day_state else {}
    return JsonResponse({"date": selected_date.isoformat(), "marks": marks})


@login_required
@require_POST
def attendance_save_state(request):
    _require_attendance_permission(request)

    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({"error": "Geçersiz veri."}, status=400)

    selected_date = _date_from_value(payload.get("date"))
    sheets = _normalize_sheets(payload.get("sheets"))
    marks = _normalize_marks(payload.get("marks"), sheets)

    with transaction.atomic():
        config, _ = AttendanceSheetConfig.objects.select_for_update().get_or_create(
            key="default",
            defaults={"sheets": sheets},
        )
        config.sheets = sheets
        config.updated_by = request.user
        config.save(update_fields=["sheets", "updated_by", "updated_at"])

        day_state, _ = AttendanceDayState.objects.select_for_update().get_or_create(
            date=selected_date,
            defaults={"marks": marks, "updated_by": request.user},
        )
        day_state.marks = marks
        day_state.updated_by = request.user
        day_state.save(update_fields=["marks", "updated_by", "updated_at"])

    return JsonResponse({
        "ok": True,
        "date": selected_date.isoformat(),
        "sheets": sheets,
        "marks": marks,
    })


@login_required
@require_POST
def attendance_leave_range(request):
    _require_attendance_permission(request)

    payload = _request_payload(request)
    if payload is None:
        return JsonResponse({"error": "Geçersiz veri."}, status=400)

    action = str(payload.get("action", "apply")).strip()
    if action not in {"apply", "remove"}:
        return JsonResponse({"error": "Geçersiz işlem."}, status=400)

    start_date = parse_date(str(payload.get("start_date", "")))
    end_date = parse_date(str(payload.get("end_date", "")))
    if not start_date or not end_date:
        return JsonResponse({"error": "Başlangıç ve bitiş tarihini seçin."}, status=400)
    if end_date < start_date:
        return JsonResponse({"error": "Bitiş tarihi başlangıçtan önce olamaz."}, status=400)

    day_count = (end_date - start_date).days + 1
    if day_count > 366:
        return JsonResponse({"error": "Tek seferde en fazla 366 gün seçebilirsiniz."}, status=400)

    config = _get_sheet_config()
    people = {person["id"]: person for person in _attendance_people(config.sheets)}
    person_id = str(payload.get("person_id", "")).strip()
    person = people.get(person_id)
    if not person:
        return JsonResponse({"error": "Geçerli bir personel seçin."}, status=400)

    selected_dates = [start_date + timedelta(days=offset) for offset in range(day_count)]
    now = timezone.now()
    changed_days = 0

    with transaction.atomic():
        existing_states = {
            state.date: state
            for state in AttendanceDayState.objects.select_for_update().filter(
                date__range=(start_date, end_date),
            )
        }
        states_to_create = []
        states_to_update = []

        for selected_date in selected_dates:
            state = existing_states.get(selected_date)
            marks = _normalize_marks(state.marks, config.sheets) if state else {}
            original_marks = deepcopy(marks)

            if action == "apply":
                marks[person_id] = {slot: "İ" for slot in ATTENDANCE_SLOTS}
            else:
                person_marks = marks.get(person_id, {})
                person_marks = {
                    slot: marker
                    for slot, marker in person_marks.items()
                    if marker != "İ"
                }
                if person_marks:
                    marks[person_id] = person_marks
                else:
                    marks.pop(person_id, None)

            if marks == original_marks:
                continue

            changed_days += 1
            if state:
                state.marks = marks
                state.updated_by = request.user
                state.updated_at = now
                states_to_update.append(state)
            else:
                states_to_create.append(AttendanceDayState(
                    date=selected_date,
                    marks=marks,
                    updated_by=request.user,
                ))

        if states_to_create:
            AttendanceDayState.objects.bulk_create(states_to_create)
        if states_to_update:
            AttendanceDayState.objects.bulk_update(
                states_to_update,
                ["marks", "updated_by", "updated_at"],
            )

    return JsonResponse({
        "ok": True,
        "action": action,
        "person_id": person_id,
        "person_name": person["name"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "day_count": day_count,
        "changed_days": changed_days,
    })
