from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import UserProfile, Answer, Question, QuestionRelationship


@receiver(pre_save, sender=Answer)
def collect_new_entry_references(sender, instance, raw=False, using='default', update_fields=None, **kwargs):
    from .entry_references import published_entry_reference_ids, referenced_entry_ids

    instance._new_entry_reference_ids = set()
    if raw or (update_fields is not None and 'answer_text' not in update_fields):
        return
    text = instance.__dict__.get('answer_text', '')
    if not referenced_entry_ids(text):
        return
    old_text = ''
    if instance.pk:
        old_text = sender.objects.using(using).filter(pk=instance.pk).values_list('answer_text', flat=True).first() or ''
    if text != old_text:
        instance._new_entry_reference_ids = (
            published_entry_reference_ids(text) - published_entry_reference_ids(old_text)
        )


@receiver(post_save, sender=Answer)
def send_new_entry_reference_notifications(sender, instance, raw=False, using='default', **kwargs):
    from .entry_references import notify_entry_references

    target_ids = instance.__dict__.pop('_new_entry_reference_ids', set())
    if not raw and target_ids:
        notify_entry_references(instance, target_ids, using=using)

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
    try:
        question = instance.question
        user = instance.user
    except Question.DoesNotExist:
        # Question zaten silinmiş (CASCADE delete), cleanup yapılmasına gerek yok
        return

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
