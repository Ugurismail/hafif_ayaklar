from django.core.management.base import BaseCommand
from django.db.models import Count

from core.models import Answer, Question, Hashtag
from core.utils import process_hashtags


class Command(BaseCommand):
    help = "Rebuild hashtag usage records from all answers and questions."

    def handle(self, *args, **options):
        self.stdout.write("Rebuilding hashtags from answers...")
        for answer in Answer.objects.all().iterator():
            process_hashtags(answer=answer)

        self.stdout.write("Rebuilding hashtags from questions...")
        for question in Question.objects.all().iterator():
            process_hashtags(question=question)

        removed, _ = Hashtag.objects.annotate(
            usage_count=Count('usages')
        ).filter(
            usage_count=0
        ).delete()

        self.stdout.write(self.style.SUCCESS("Hashtag rebuild complete."))
        self.stdout.write(f"Removed {removed} unused hashtag records.")
