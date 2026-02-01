"""
Hashtag and mention views
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from core.models import Hashtag, HashtagUsage, Answer, Question
from django.http import JsonResponse


def hashtag_view(request, hashtag_name):
    """
    Display all answers and questions tagged with a specific hashtag
    """
    hashtag = get_object_or_404(Hashtag, name=hashtag_name.lower())

    # Get all usages for this hashtag
    usages = HashtagUsage.objects.filter(hashtag=hashtag).select_related(
        'answer__user', 'answer__question',
        'question__user'
    ).order_by('-created_at')

    # Combine answers and questions
    items = []
    for usage in usages:
        if usage.answer:
            items.append({
                'type': 'answer',
                'object': usage.answer,
                'question': usage.answer.question,
                'user': usage.answer.user,
                'created_at': usage.answer.created_at,
            })
        elif usage.question:
            items.append({
                'type': 'question',
                'object': usage.question,
                'user': usage.question.user,
                'created_at': usage.question.created_at,
            })

    # Sort by created_at
    items.sort(key=lambda x: x['created_at'], reverse=True)

    # Pagination
    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'hashtag': hashtag,
        'page_obj': page_obj,
        'usage_count': len(items),
    }

    return render(request, 'core/hashtag_detail.html', context)


def trending_hashtags(request):
    """
    Display trending hashtags (most used in last 7 days)
    """
    from datetime import timedelta
    from django.utils import timezone

    seven_days_ago = timezone.now() - timedelta(days=7)

    # Get hashtags used in last 7 days with usage count
    hashtags = Hashtag.objects.filter(
        usages__created_at__gte=seven_days_ago
    ).annotate(
        usage_count=Count('usages')
    ).order_by('-usage_count')[:50]

    context = {
        'hashtags': hashtags,
    }

    return render(request, 'core/trending_hashtags.html', context)


def all_hashtags(request):
    """
    Display all hashtags alphabetically with pagination
    """
    hashtags = Hashtag.objects.annotate(
        usage_count=Count('usages')
    ).filter(usage_count__gt=0).order_by('name')

    # Pagination for all hashtags list
    paginator = Paginator(list(hashtags), 50)  # 50 hashtags per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Group paginated hashtags by first letter
    hashtag_dict = {}
    for hashtag in page_obj:
        first_letter = hashtag.name[0].upper()
        if first_letter not in hashtag_dict:
            hashtag_dict[first_letter] = []
        hashtag_dict[first_letter].append(hashtag)

    context = {
        'hashtag_dict': sorted(hashtag_dict.items()),
        'total_count': hashtags.count(),
        'page_obj': page_obj,
    }

    return render(request, 'core/all_hashtags.html', context)


@login_required
def search_hashtags(request):
    """
    AJAX search for hashtags (for autocomplete)
    """
    query = request.GET.get('q', '').strip().lower()

    if not query:
        return JsonResponse({'hashtags': []})

    hashtags = Hashtag.objects.filter(
        name__icontains=query
    ).annotate(
        usage_count=Count('usages')
    ).filter(
        usage_count__gt=0
    ).order_by('-usage_count')[:10]

    results = [{
        'name': h.name,
        'usage_count': h.usage_count,
    } for h in hashtags]

    return JsonResponse({'hashtags': results})
