"""
Core service layer
Business logic extracted from views for reusability
"""

from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from .models import Vote, SavedItem


class VoteSaveService:
    """
    Service class for handling vote and save-related queries
    Eliminates duplicate code across views
    """

    @staticmethod
    def annotate_user_votes(items, user, model_class):
        """
        Add user_vote_value attribute to each item in the list

        Args:
            items: List or QuerySet of model instances
            user: User object
            model_class: Model class (e.g., Answer, Question)

        Returns:
            Same items list with user_vote_value attribute added

        Example:
            VoteSaveService.annotate_user_votes(answers, request.user, Answer)
        """
        # For anonymous users, set all votes to 0
        if not user.is_authenticated:
            for item in items:
                item.user_vote_value = 0
            return items

        content_type = ContentType.objects.get_for_model(model_class)
        item_ids = [item.id for item in items]

        # Get user's votes for these items
        user_votes = Vote.objects.filter(
            user=user,
            content_type=content_type,
            object_id__in=item_ids
        ).values('object_id', 'value')

        # Create lookup dictionary
        vote_dict = {vote['object_id']: vote['value'] for vote in user_votes}

        # Annotate items
        for item in items:
            item.user_vote_value = vote_dict.get(item.id, 0)

        return items

    @staticmethod
    def get_save_info(items, user, model_class):
        """
        Get save information for a list of items

        Args:
            items: List or QuerySet of model instances
            user: User object
            model_class: Model class (e.g., Answer, Question)

        Returns:
            Tuple of (saved_ids_set, save_count_dict)
            - saved_ids_set: Set of IDs saved by current user
            - save_count_dict: Dict mapping item_id -> total save count

        Example:
            saved_ids, save_dict = VoteSaveService.get_save_info(answers, request.user, Answer)
        """
        content_type = ContentType.objects.get_for_model(model_class)
        item_ids = [item.id for item in items]

        # Get IDs of items saved by current user
        if user.is_authenticated:
            saved_ids = set(SavedItem.objects.filter(
                user=user,
                content_type=content_type,
                object_id__in=item_ids
            ).values_list('object_id', flat=True))
        else:
            saved_ids = set()

        # Get total save counts for all items
        save_counts = SavedItem.objects.filter(
            content_type=content_type,
            object_id__in=item_ids
        ).values('object_id').annotate(count=Count('id'))

        save_dict = {item['object_id']: item['count'] for item in save_counts}

        return saved_ids, save_dict

    @staticmethod
    def get_user_saved_ids(user, model_class, item_ids):
        """
        Get IDs of items saved by a specific user

        Args:
            user: User object
            model_class: Model class
            item_ids: List of item IDs to check

        Returns:
            Set of saved item IDs
        """
        if not user.is_authenticated:
            return set()

        content_type = ContentType.objects.get_for_model(model_class)
        return set(SavedItem.objects.filter(
            user=user,
            content_type=content_type,
            object_id__in=item_ids
        ).values_list('object_id', flat=True))

    @staticmethod
    def get_save_counts(model_class, item_ids):
        """
        Get save counts for a list of items

        Args:
            model_class: Model class
            item_ids: List of item IDs

        Returns:
            Dict mapping item_id -> save count
        """
        content_type = ContentType.objects.get_for_model(model_class)

        save_counts = SavedItem.objects.filter(
            content_type=content_type,
            object_id__in=item_ids
        ).values('object_id').annotate(count=Count('id'))

        return {item['object_id']: item['count'] for item in save_counts}
