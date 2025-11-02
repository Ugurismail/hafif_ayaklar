"""
Utility functions for mention, hashtag processing and pagination
"""
import re
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Notification, Hashtag, HashtagUsage


def paginate_queryset(queryset, request, page_param='page', per_page=20):
    """
    Paginate a queryset

    Args:
        queryset: QuerySet to paginate
        request: HTTP request object
        page_param: GET parameter name for page number (default: 'page')
        per_page: Number of items per page (default: 20)

    Returns:
        Paginated page object
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(page_param, 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


def extract_mentions(text):
    """
    Extract all @mentions from text
    Returns list of usernames (without @)
    Supports multi-word usernames by checking database
    """
    # Pattern: @ ile başlayan ve sonrasında max 50 karakter (boşluk dahil)
    pattern = r'@([A-Za-z0-9_.\\-ğüşöçıİĞÜŞÖÇ ]{1,50})'

    found_usernames = []
    matches = re.finditer(pattern, text)

    for match in matches:
        candidate = match.group(1).strip()
        words = candidate.split()

        # Try from longest match to shortest (max 3 words)
        for i in range(min(len(words), 3), 0, -1):
            username = ' '.join(words[:i])
            try:
                # Check if user exists in database
                User.objects.get(username__iexact=username)
                found_usernames.append(username)
                break  # Found valid username, stop checking shorter versions
            except User.DoesNotExist:
                continue

    return list(set(found_usernames))  # Remove duplicates


def extract_hashtags(text):
    """
    Extract all #hashtags from text
    Returns list of hashtag names (without #)
    """
    # Pattern: #hashtag (alphanumeric, underscore)
    # Must not be preceded by alphanumeric to avoid matching mid-word
    pattern = r'(?:^|[^a-zA-Z0-9_])#([a-zA-Z0-9_]+)'
    hashtags = re.findall(pattern, text)
    return list(set([h.lower() for h in hashtags]))  # Lowercase and remove duplicates


def send_mention_notifications(answer, mentioned_usernames):
    """
    Send mention notifications to users
    Creates Notification objects for each mentioned user
    """
    author = answer.user

    for username in mentioned_usernames:
        try:
            mentioned_user = User.objects.get(username=username)

            # Don't send notification if user mentions themselves
            if mentioned_user == author:
                continue

            # Create mention notification
            Notification.create_mention_notification(
                recipient=mentioned_user,
                sender=author,
                answer=answer
            )
        except User.DoesNotExist:
            # User doesn't exist, skip
            continue


def process_hashtags(answer=None, question=None):
    """
    Process hashtags in answer or question text
    Creates Hashtag and HashtagUsage objects
    """
    if answer:
        text = answer.answer_text
    elif question:
        text = question.question_text
    else:
        return

    hashtag_names = extract_hashtags(text)

    for hashtag_name in hashtag_names:
        # Get or create hashtag
        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)

        # Create usage record if it doesn't exist
        if answer:
            HashtagUsage.objects.get_or_create(
                hashtag=hashtag,
                answer=answer
            )
        elif question:
            HashtagUsage.objects.get_or_create(
                hashtag=hashtag,
                question=question
            )


def link_mentions_in_text(text):
    """
    Convert @mentions to clickable links in HTML
    """
    def replace_mention(match):
        username = match.group(1)
        return f'<a href="/profile/{username}/" class="mention-link">@{username}</a>'

    pattern = r'@([a-zA-Z0-9_-]+)'
    return re.sub(pattern, replace_mention, text)


def link_hashtags_in_text(text):
    """
    Convert #hashtags to clickable links in HTML
    """
    def replace_hashtag(match):
        hashtag = match.group(1)
        return f'<a href="/hashtag/{hashtag.lower()}/" class="hashtag-link">#{hashtag}</a>'

    pattern = r'(?:^|[^a-zA-Z0-9_])(#([a-zA-Z0-9_]+))'

    def replace_full(match):
        prefix = match.group(0)[0] if len(match.group(0)) > 1 and match.group(0)[0] != '#' else ''
        hashtag = match.group(2)
        return f'{prefix}<a href="/hashtag/{hashtag.lower()}/" class="hashtag-link">#{hashtag}</a>'

    return re.sub(pattern, replace_full, text)
