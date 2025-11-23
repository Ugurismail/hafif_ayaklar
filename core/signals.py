from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile, Answer, Question, QuestionRelationship

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            invitation_quota = 999999999
        else:
            invitation_quota = 0
        UserProfile.objects.create(user=instance, invitation_quota=invitation_quota)


@receiver(post_delete, sender=Answer)
def cleanup_question_relationships_on_answer_delete(sender, instance, **kwargs):
    """
    Entry silindiğinde:
    1. Kullanıcının o soruda başka entry'si yoksa
    2. O kullanıcının bu soruyla ilgili TÜM QuestionRelationship'lerini sil
       - Bu sorunun parent olduğu ilişkiler (soru → X)
       - Bu sorunun child olduğu ilişkiler (X → soru)
    3. question.users'dan kullanıcıyı çıkar
    4. Eğer bu sorunun hiç entry'si kalmadıysa, soruyu da sil
    """
    question = instance.question
    user = instance.user

    # Bu kullanıcının bu soruda başka entry'si var mı?
    has_other_entries = Answer.objects.filter(question=question, user=user).exists()

    if not has_other_entries:
        # Bu kullanıcının bu soruyla ilgili TÜM ilişkilerini sil
        QuestionRelationship.objects.filter(
            parent=question,
            user=user
        ).delete()

        QuestionRelationship.objects.filter(
            child=question,
            user=user
        ).delete()

        # question.users'dan kullanıcıyı çıkar
        question.users.remove(user)

    # Eğer bu sorunun hiç entry'si kalmadıysa, soruyu da sil
    if not Answer.objects.filter(question=question).exists():
        question.delete()
