from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import signals
from core.models import (
    Question, Answer, Poll, PollOption, PollVote,
    RandomSentence, DelphoiProphecy, DelphoiRequest, Hashtag, HashtagUsage,
    Notification, Message, QuestionRelationship,
    QuestionFollow, AnswerFollow, SavedItem, Vote, PinnedEntry
)
import core.signals  # Import to ensure signals are registered


class Command(BaseCommand):
    help = 'Clears all test data but keeps admin user and References'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🧹 Starting data cleanup...'))
        self.stdout.write(self.style.WARNING('⚠️  This will delete everything except admin user and References!'))

        confirm = input('Are you sure? Type "yes" to continue: ')
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.ERROR('❌ Aborted.'))
            return

        # Temporarily disable signals to avoid issues during cascade delete
        self.stdout.write(self.style.WARNING('⚠️  Temporarily disabling signals...'))
        signals.post_delete.disconnect(core.signals.cleanup_question_relationships_on_answer_delete, sender=Answer)

        # Delete Questions and related data
        question_count = Question.objects.count()
        Question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {question_count} questions (and related answers)'))

        # Delete Answers (if any remain)
        answer_count = Answer.objects.count()
        Answer.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {answer_count} remaining answers'))

        # Delete Polls and related
        poll_count = Poll.objects.count()
        Poll.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {poll_count} polls'))

        pollvote_count = PollVote.objects.count()
        PollVote.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {pollvote_count} poll votes'))

        polloption_count = PollOption.objects.count()
        PollOption.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {polloption_count} poll options'))

        # Delete RandomSentence
        sentence_count = RandomSentence.objects.count()
        RandomSentence.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {sentence_count} random sentences'))

        # Delete Prophecies and Requests
        prophecy_count = DelphoiProphecy.objects.count()
        DelphoiProphecy.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {prophecy_count} prophecies'))

        delphoi_req_count = DelphoiRequest.objects.count()
        DelphoiRequest.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {delphoi_req_count} delphoi requests'))

        # Delete Hashtags and usages
        hashtag_count = Hashtag.objects.count()
        Hashtag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {hashtag_count} hashtags'))

        hashtagusage_count = HashtagUsage.objects.count()
        HashtagUsage.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {hashtagusage_count} hashtag usages'))

        # Delete Notifications
        notification_count = Notification.objects.count()
        Notification.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {notification_count} notifications'))

        # Delete Messages
        message_count = Message.objects.count()
        Message.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {message_count} messages'))

        # Delete Question/Answer follows
        follow_q_count = QuestionFollow.objects.count()
        QuestionFollow.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {follow_q_count} question follows'))

        follow_a_count = AnswerFollow.objects.count()
        AnswerFollow.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {follow_a_count} answer follows'))

        # Delete SavedItems, Votes, PinnedEntries
        saved_count = SavedItem.objects.count()
        SavedItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {saved_count} saved items'))

        vote_count = Vote.objects.count()
        Vote.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {vote_count} votes'))

        pinned_count = PinnedEntry.objects.count()
        PinnedEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {pinned_count} pinned entries'))

        # Delete Question relationships
        qrel_count = QuestionRelationship.objects.count()
        QuestionRelationship.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {qrel_count} question relationships'))

        # Delete non-admin users and their profiles
        admin_users = User.objects.filter(is_superuser=True)
        non_admin_users = User.objects.exclude(is_superuser=True)
        user_count = non_admin_users.count()
        non_admin_users.delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {user_count} non-admin users'))

        # Clear admin user's follower/following relationships
        for admin in admin_users:
            if hasattr(admin, 'userprofile'):
                admin.userprofile.followers.clear()
                admin.userprofile.following.clear()
                self.stdout.write(self.style.SUCCESS(f'✅ Cleared admin ({admin.username}) follower relationships'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Cleanup complete!'))
        self.stdout.write(self.style.SUCCESS('✅ Admin users: KEPT'))
        self.stdout.write(self.style.SUCCESS('✅ References: KEPT'))
        self.stdout.write(self.style.SUCCESS('❌ Everything else: DELETED'))
