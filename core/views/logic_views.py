from functools import lru_cache
from importlib import import_module

from django.http import Http404
from django.shortcuts import redirect, render


@lru_cache(maxsize=1)
def _logic_course_data():
    return import_module("core.logic_course_data")


@lru_cache(maxsize=1)
def _logic_level_test_bank():
    return import_module("core.logic_level_test_bank")


def logic_home(request):
    course = _logic_course_data().get_logic_course()
    lessons = course["lessons"]
    return render(
        request,
        "core/logic_home.html",
        {
            "logic_levels": course["levels"],
            "logic_model": course["teaching_model"],
            "logic_lessons": lessons,
            "active_logic_lessons": course["active_lesson_count"],
            "logic_hero": course["hero"],
            "logic_test_bank_size": _logic_level_test_bank().get_logic_level_test_bank_size(),
        },
    )


def logic_lesson_detail(request, lesson_slug):
    lesson, redirect_slug = _logic_course_data().resolve_logic_lesson(lesson_slug)
    if redirect_slug:
        return redirect("logic_lesson_detail", lesson_slug=redirect_slug)
    if not lesson:
        raise Http404("Mantık dersi bulunamadı.")
    if not lesson.get("active"):
        raise Http404("Bu mantık dersi henüz açık değil.")
    return render(
        request,
        "core/logic_lesson_detail.html",
        {
            "lesson": lesson,
            "logic_test_available": _logic_level_test_bank().get_logic_level_test_bank_size() > 0,
        },
    )


def logic_level_test(request):
    assessment = _logic_level_test_bank().build_logic_level_test()
    if not assessment:
        raise Http404("Mantık bitirme testi bulunamadı.")

    return render(
        request,
        "core/logic_level_test.html",
        {
            "assessment": assessment,
        },
    )
