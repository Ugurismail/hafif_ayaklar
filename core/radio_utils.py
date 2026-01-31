from django.utils import timezone

from .models import RadioProgram


def expire_live_programs(now=None):
    """Stop any live programs that passed their end_time."""
    current_time = now or timezone.now()
    return RadioProgram.objects.filter(
        is_live=True,
        end_time__lt=current_time
    ).update(is_live=False, is_finished=True)
