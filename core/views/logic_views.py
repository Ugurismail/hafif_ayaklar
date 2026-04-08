from django.http import Http404
from django.shortcuts import redirect, render

from ..logic_course_data import get_logic_course, resolve_logic_lesson
from ..logic_level_test_bank import build_logic_level_test, get_logic_level_test_bank_size


def logic_home(request):
    course = get_logic_course()
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
            "logic_test_bank_size": get_logic_level_test_bank_size(),
        },
    )


def logic_lesson_detail(request, lesson_slug):
    lesson, redirect_slug = resolve_logic_lesson(lesson_slug)
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
            "logic_test_available": get_logic_level_test_bank_size() > 0,
        },
    )


def logic_level_test(request):
    assessment = build_logic_level_test()
    if not assessment:
        raise Http404("Mantık bitirme testi bulunamadı.")

    return render(
        request,
        "core/logic_level_test.html",
        {
            "assessment": assessment,
        },
    )
