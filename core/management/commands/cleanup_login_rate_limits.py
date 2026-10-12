from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import LoginRateLimitBucket


class Command(BaseCommand):
    help = 'Delete expired login rate limit buckets in bounded batches.'

    def handle(self, *args, **options):
        cutoff = timezone.now()
        total = 0
        while True:
            keys = list(LoginRateLimitBucket.objects.filter(expires_at__lte=cutoff)
                        .order_by('expires_at').values_list('pk', flat=True)[:500])
            if not keys:
                break
            # Recheck expiry so a concurrently renewed bucket is never deleted.
            deleted, _ = LoginRateLimitBucket.objects.filter(pk__in=keys, expires_at__lte=cutoff).delete()
            total += deleted
        self.stdout.write(f'Deleted {total} expired login rate limit buckets.')
