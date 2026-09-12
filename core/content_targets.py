"""Validation shared by public-content vote/save endpoints."""

from django.contrib.contenttypes.models import ContentType

from .models import Answer, Question, SavedCollection


def positive_object_id(value):
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise ValueError('Invalid object_id') from None
    if not 0 < result <= 2147483647:
        raise ValueError('Invalid object_id')
    return result


def public_content_target(content_type, object_id):
    model = {'question': Question, 'answer': Answer}.get(content_type)
    if model is None:
        raise ValueError('Invalid content_type')
    pk = positive_object_id(object_id)
    return model, ContentType.objects.get_for_model(model), pk


def owned_collections(user, raw_ids):
    ids = {positive_object_id(value) for value in raw_ids}
    collections = list(SavedCollection.objects.filter(user=user, pk__in=ids).order_by('pk'))
    if len(collections) != len(ids):
        raise ValueError('Invalid collection selection')
    return collections
