import json
import secrets
from copy import deepcopy
from functools import lru_cache
from importlib import import_module

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.logic_curriculum import LOGIC_MASTERY_THRESHOLD
from core.logic_interactives import get_logic_interactive
from core.models import LogicLessonProgress


@lru_cache(maxsize=1)
def _logic_course_data():
    return import_module("core.logic_course_data")


@lru_cache(maxsize=1)
def _logic_level_test_bank():
    return import_module("core.logic_level_test_bank")


def _decorate_course_progress(request, course):
    progress_by_slug = {}
    if request.user.is_authenticated:
        progress_by_slug = {
            item.lesson_slug: item
            for item in LogicLessonProgress.objects.filter(user=request.user)
        }

    completed_count = 0
    started_count = 0
    for lesson in course["lessons"]:
        progress = progress_by_slug.get(lesson["slug"])
        lesson["progress_status"] = progress.status if progress else "not_started"
        lesson["best_score"] = progress.best_score if progress else 0
        lesson["attempt_count"] = progress.attempt_count if progress else 0
        lesson["is_completed"] = bool(
            progress and progress.status == LogicLessonProgress.STATUS_COMPLETED
        )
        lesson["is_started"] = bool(
            progress and progress.status == LogicLessonProgress.STATUS_STARTED
        )
        completed_count += int(lesson["is_completed"])
        started_count += int(lesson["is_started"])

    lesson_by_slug = {lesson["slug"]: lesson for lesson in course["lessons"]}
    for stage in course["levels"]:
        stage_completed = 0
        for stage_lesson in stage["lessons"]:
            decorated = lesson_by_slug[stage_lesson["slug"]]
            stage_lesson.update(
                {
                    "progress_status": decorated["progress_status"],
                    "best_score": decorated["best_score"],
                    "attempt_count": decorated["attempt_count"],
                    "is_completed": decorated["is_completed"],
                    "is_started": decorated["is_started"],
                }
            )
            stage_completed += int(decorated["is_completed"])
        stage["completed_count"] = stage_completed
        stage["progress_percent"] = round(
            (stage_completed / max(stage["lesson_count"], 1)) * 100
        )

    recent_incomplete = [
        progress
        for progress in progress_by_slug.values()
        if progress.status != LogicLessonProgress.STATUS_COMPLETED
        and progress.lesson_slug in lesson_by_slug
    ]
    if recent_incomplete:
        recent_incomplete.sort(key=lambda item: item.last_opened_at, reverse=True)
        continue_lesson = lesson_by_slug[recent_incomplete[0].lesson_slug]
    else:
        continue_lesson = next(
            (lesson for lesson in course["lessons"] if not lesson["is_completed"]),
            course["lessons"][0] if course["lessons"] else None,
        )

    for stage in course["levels"]:
        stage["is_current"] = bool(
            continue_lesson and continue_lesson["stage_id"] == stage["id"]
        )

    total = len(course["lessons"])
    return {
        "logic_continue_lesson": continue_lesson,
        "logic_progress": {
            "completed": completed_count,
            "started": started_count,
            "total": total,
            "percent": round((completed_count / max(total, 1)) * 100),
        },
    }


def logic_home(request):
    course = _logic_course_data().get_logic_course()
    lessons = course["lessons"]
    progress_context = _decorate_course_progress(request, course)
    return render(
        request,
        "core/logic_home.html",
        {
            "logic_levels": course["levels"],
            "logic_model": course["teaching_model"],
            "logic_lessons": lessons,
            "logic_pathways": course["pathways"],
            "logic_sources": course["sources"],
            "logic_curriculum_version": course["curriculum_version"],
            "logic_mastery_threshold": course["mastery_threshold"],
            "active_logic_lessons": course["active_lesson_count"],
            "logic_hero": course["hero"],
            "logic_test_bank_size": _logic_level_test_bank().get_logic_level_test_bank_size(),
            **progress_context,
        },
    )


def _candidate_review_context(
    lessons,
    source_references,
    lesson_lookup,
    *,
    stage_code,
    stage_title,
    lesson_range,
):
    candidate_lessons = deepcopy(lessons)
    current_stage_slugs = {lesson["slug"] for lesson in candidate_lessons}
    for lesson in candidate_lessons:
        lesson["prerequisite_details"] = [
            {
                "curriculum_id": lesson_lookup[slug]["curriculum_id"],
                "title": lesson_lookup[slug]["title"],
                "in_review_stage": slug in current_stage_slugs,
            }
            for slug in lesson["prerequisites"]
        ]
        lesson["source_details"] = [
            source_references[source_id]
            for source_id in lesson["source_ids"]
        ]

    return {
        "candidate_lessons": candidate_lessons,
        "candidate_total_minutes": sum(
            lesson["estimated_minutes"] for lesson in candidate_lessons
        ),
        "candidate_practice_count": sum(
            len(lesson["practice"]) for lesson in candidate_lessons
        ),
        "candidate_production_count": sum(
            len(lesson["production_tasks"]) for lesson in candidate_lessons
        ),
        "review_stage_code": stage_code,
        "review_stage_title": stage_title,
        "review_lesson_range": lesson_range,
    }


@staff_member_required
def logic_stage_a_preview(request):
    """Render the isolated Stage A candidate for human curriculum review."""
    from core.logic_phase3_stage_a import (
        STAGE_A_CANDIDATE_LESSONS,
        STAGE_A_SOURCE_REFERENCES,
    )

    return render(
        request,
        "core/logic_stage_a_preview.html",
        _candidate_review_context(
            STAGE_A_CANDIDATE_LESSONS,
            STAGE_A_SOURCE_REFERENCES,
            {
                lesson["slug"]: lesson
                for lesson in STAGE_A_CANDIDATE_LESSONS
            },
            stage_code="Faz 3A",
            stage_title="Mantıksal okuryazarlık",
            lesson_range="A1-A6",
        ),
    )


@staff_member_required
def logic_stage_b_preview(request):
    """Render the isolated Stage B candidate for human curriculum review."""
    from core.logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
    from core.logic_phase3_stage_b import (
        STAGE_B_CANDIDATE_LESSONS,
        STAGE_B_CANDIDATE_MAP,
        STAGE_B_SOURCE_REFERENCES,
    )

    return render(
        request,
        "core/logic_stage_a_preview.html",
        _candidate_review_context(
            STAGE_B_CANDIDATE_LESSONS,
            STAGE_B_SOURCE_REFERENCES,
            {**STAGE_A_CANDIDATE_MAP, **STAGE_B_CANDIDATE_MAP},
            stage_code="Faz 3B",
            stage_title="TFL dili ve sembolleştirme",
            lesson_range="B7-B13",
        ),
    )


@staff_member_required
def logic_stage_c_preview(request):
    """Render the isolated Stage C candidate for human curriculum review."""
    from core.logic_phase3_stage_a import STAGE_A_CANDIDATE_MAP
    from core.logic_phase3_stage_b import STAGE_B_CANDIDATE_MAP
    from core.logic_phase3_stage_c import (
        STAGE_C_CANDIDATE_LESSONS,
        STAGE_C_CANDIDATE_MAP,
        STAGE_C_SOURCE_REFERENCES,
    )

    return render(
        request,
        "core/logic_stage_a_preview.html",
        _candidate_review_context(
            STAGE_C_CANDIDATE_LESSONS,
            STAGE_C_SOURCE_REFERENCES,
            {
                **STAGE_A_CANDIDATE_MAP,
                **STAGE_B_CANDIDATE_MAP,
                **STAGE_C_CANDIDATE_MAP,
            },
            stage_code="Faz 3C",
            stage_title="TFL semantiği ve yöntem seçimi",
            lesson_range="C14-C19",
        ),
    )


def logic_lesson_detail(request, lesson_slug):
    lesson, redirect_slug = _logic_course_data().resolve_logic_lesson(lesson_slug)
    if redirect_slug:
        return redirect("logic_lesson_detail", lesson_slug=redirect_slug, permanent=True)
    if not lesson:
        raise Http404("Mantık dersi bulunamadı.")
    if not lesson.get("active"):
        raise Http404("Bu mantık dersi henüz açık değil.")
    progress = None
    if request.user.is_authenticated:
        stage_slugs = [item["slug"] for item in lesson["stage_lessons"]]
        stage_progress = {
            item.lesson_slug: item
            for item in LogicLessonProgress.objects.filter(
                user=request.user,
                lesson_slug__in=stage_slugs,
            )
        }
        progress = stage_progress.get(lesson["slug"])
        for stage_lesson in lesson["stage_lessons"]:
            item_progress = stage_progress.get(stage_lesson["slug"])
            stage_lesson["progress_status"] = (
                item_progress.status if item_progress else LogicLessonProgress.STATUS_NOT_STARTED
            )
            stage_lesson["best_score"] = item_progress.best_score if item_progress else 0
    else:
        for stage_lesson in lesson["stage_lessons"]:
            stage_lesson["progress_status"] = LogicLessonProgress.STATUS_NOT_STARTED
            stage_lesson["best_score"] = 0

    return render(
        request,
        "core/logic_lesson_detail.html",
        {
            "lesson": lesson,
            "logic_progress": progress,
            "logic_interactive": get_logic_interactive(lesson["slug"]),
            "logic_mastery_threshold": LOGIC_MASTERY_THRESHOLD,
            "logic_test_available": _logic_level_test_bank().get_logic_level_test_bank_size() > 0,
        },
    )


def logic_level_test(request):
    session_key = "logic_level_test_seed"
    if request.GET.get("yeni") == "1":
        request.session[session_key] = secrets.token_hex(12)
        return redirect("logic_level_test")

    seed = request.session.get(session_key)
    if not seed:
        seed = secrets.token_hex(12)
        request.session[session_key] = seed

    assessment = _logic_level_test_bank().build_logic_level_test(seed=seed)
    if not assessment:
        raise Http404("Mantık bitirme testi bulunamadı.")

    return render(
        request,
        "core/logic_level_test.html",
        {
            "assessment": assessment,
        },
    )


@require_POST
def logic_lesson_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"ok": False, "error": "İlerlemeyi hesabına kaydetmek için giriş yapmalısın."},
            status=401,
        )

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "Geçersiz istek."}, status=400)

    lesson_slug = str(payload.get("lesson_slug", "")).strip()
    action = str(payload.get("action", "opened")).strip()
    lesson = _logic_course_data().get_logic_lesson(lesson_slug)
    if not lesson:
        return JsonResponse({"ok": False, "error": "Ders bulunamadı."}, status=404)
    if action not in {"opened", "graded"}:
        return JsonResponse({"ok": False, "error": "Geçersiz ilerleme işlemi."}, status=400)

    score = None
    if action == "graded":
        try:
            score = int(payload.get("score"))
        except (TypeError, ValueError):
            return JsonResponse({"ok": False, "error": "Puan belirtilmedi."}, status=400)
        if not 0 <= score <= 100:
            return JsonResponse({"ok": False, "error": "Puan 0 ile 100 arasında olmalı."}, status=400)

    mastery_threshold = LOGIC_MASTERY_THRESHOLD
    with transaction.atomic():
        progress, _ = LogicLessonProgress.objects.select_for_update().get_or_create(
            user=request.user,
            lesson_slug=lesson_slug,
            defaults={"status": LogicLessonProgress.STATUS_STARTED},
        )

        if action == "opened" and progress.status == LogicLessonProgress.STATUS_NOT_STARTED:
            progress.status = LogicLessonProgress.STATUS_STARTED
        elif action == "graded":
            progress.last_score = score
            progress.best_score = max(progress.best_score, score)
            progress.attempt_count += 1
            if score >= mastery_threshold:
                progress.status = LogicLessonProgress.STATUS_COMPLETED
                progress.completed_at = progress.completed_at or timezone.now()
            elif progress.status != LogicLessonProgress.STATUS_COMPLETED:
                progress.status = LogicLessonProgress.STATUS_STARTED
        progress.save()

    return JsonResponse(
        {
            "ok": True,
            "lesson_slug": progress.lesson_slug,
            "status": progress.status,
            "last_score": progress.last_score,
            "best_score": progress.best_score,
            "attempt_count": progress.attempt_count,
            "mastery_threshold": mastery_threshold,
        }
    )
