from functools import lru_cache
from importlib import import_module

from django.http import Http404
from django.shortcuts import render


@lru_cache(maxsize=1)
def _german_course_data():
    return import_module("core.german_course_data")


@lru_cache(maxsize=1)
def _german_level_test_bank():
    return import_module("core.german_level_test_bank")


def german_course_home(request):
    course_data = _german_course_data()
    test_bank = _german_level_test_bank()

    levels = course_data.get_german_course_overview()
    total_lessons = sum(level["lesson_count"] for level in course_data.GERMAN_COURSE_LEVELS)
    live_lessons = sum(level["available_lessons"] for level in levels)
    a1_live_lessons = next((level["available_lessons"] for level in levels if level["slug"] == "a1"), 0)
    a2_live_lessons = next((level["available_lessons"] for level in levels if level["slug"] == "a2"), 0)
    a1_test_bank_size = test_bank.get_level_test_bank_size("a1")
    a2_test_bank_size = test_bank.get_level_test_bank_size("a2")
    live_level_titles = [level["title"] for level in levels if level["available_lessons"]]
    live_level_summary = " + ".join(live_level_titles) if live_level_titles else "Henüz açık seviye yok"

    return render(
        request,
        "core/german_course_home.html",
        {
            "course_levels": levels,
            "course_totals": {
                "planned_levels": len(levels),
                "planned_lessons": total_lessons,
                "live_lessons": live_lessons,
            },
            "a1_live_lessons": a1_live_lessons,
            "a2_live_lessons": a2_live_lessons,
            "a1_scope_matrix": course_data.A1_SCOPE_MATRIX,
            "a2_scope_matrix": course_data.A2_SCOPE_MATRIX,
            "a1_test_bank_size": a1_test_bank_size,
            "a2_test_bank_size": a2_test_bank_size,
            "live_level_summary": live_level_summary,
        },
    )


def german_lesson_detail(request, level_slug, lesson_slug):
    course_data = _german_course_data()
    test_bank = _german_level_test_bank()

    lesson = course_data.get_german_lesson(level_slug, lesson_slug)
    if not lesson:
        raise Http404("Ders bulunamadi.")

    level = next((item for item in course_data.GERMAN_COURSE_LEVELS if item["slug"] == level_slug), None)
    if not level:
        raise Http404("Seviye bulunamadi.")

    lesson_list = course_data.GERMAN_LESSONS.get(level_slug, [])
    current_index = next((idx for idx, item in enumerate(lesson_list) if item["slug"] == lesson_slug), None)
    previous_lesson = lesson_list[current_index - 1] if current_index not in {None, 0} else None
    next_level_lesson = (
        lesson_list[current_index + 1]
        if current_index is not None and current_index + 1 < len(lesson_list)
        else None
    )
    level_lessons = [
        {
            "index": item["index"],
            "title": item["title"],
            "slug": item["slug"],
            "is_current": item["slug"] == lesson_slug,
        }
        for item in lesson_list
    ]

    return render(
        request,
        "core/german_lesson_detail.html",
        {
            "lesson": lesson,
            "level": level,
            "level_lessons": level_lessons,
            "previous_lesson": previous_lesson,
            "next_level_lesson": next_level_lesson,
            "level_test_available": test_bank.get_level_test_bank_size(level_slug) > 0,
        },
    )


def german_level_test(request, level_slug):
    course_data = _german_course_data()
    test_bank = _german_level_test_bank()

    level = next((item for item in course_data.GERMAN_COURSE_LEVELS if item["slug"] == level_slug), None)
    if not level:
        raise Http404("Seviye bulunamadi.")

    assessment = test_bank.build_german_level_test(level_slug)
    if not assessment:
        raise Http404("Seviye testi bulunamadi.")

    return render(
        request,
        "core/german_level_test.html",
        {
            "assessment": assessment,
            "level": level,
        },
    )
