from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
import datetime
from django.conf import settings
import re
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .validators import validate_image_file




class Invitation(models.Model):
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_invitations', null=True, blank=True
    )
    quota_granted = models.PositiveIntegerField(default=0)  # Eklendi
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='used_invitations', null=True, blank=True
    )

    def __str__(self):
        return f"Invitation from {self.sender.username if self.sender else 'System'}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invitation_quota = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, validators=[validate_image_file])

    # Radyo DJ yetkisi
    is_dj = models.BooleanField(default=False, verbose_name='DJ Yetkisi')

    # Renk ayarları alanları
    background_color = models.CharField(max_length=7, default='#F5F5F5') #genel arka plan
    text_color = models.CharField(max_length=7, default='#000000')
    message_bubble_color = models.CharField(max_length=7, default='#d1e7ff')
    tbas_color=models.CharField(max_length=7, default='#000000')

    yanit_card = models.CharField(max_length=7, default='#ffffff')
    header_background_color = models.CharField(max_length=7, default='#ffffff')
    header_text_color = models.CharField(max_length=7, default='#333333')
    link_color = models.CharField(max_length=7, default='#6E8CA7')
    link_hover_color = models.CharField(max_length=7, default='#4E647E')

    button_background_color = models.CharField(max_length=7, default='#6E8CA7')
    button_hover_background_color = models.CharField(max_length=7, default='#4E647E')
    button_text_color = models.CharField(max_length=7, default='#ffffff')

    secondary_button_background_color = models.CharField(max_length=7, default='#6c757d')
    secondary_button_hover_background_color = models.CharField(max_length=7, default='#495057')
    secondary_button_text_color = models.CharField(max_length=7, default='#ffffff')

    font_size = models.IntegerField(default=16)

    hover_background_color = models.CharField(max_length=7, default='#f0f0f0')
    icon_color = models.CharField(max_length=7, default='#333333')
    icon_hover_color = models.CharField(max_length=7, default='#007bff')
    answer_background_color = models.CharField(max_length=7, default='#F5F5F5')
    content_background_color = models.CharField(max_length=7, default='#ffffff')
    tab_background_color = models.CharField(max_length=7, default='#f8f9fa')
    tab_text_color = models.CharField(max_length=7, default='#000000')
    tab_active_background_color = models.CharField(max_length=7, default='#ffffff')
    tab_active_text_color = models.CharField(max_length=7, default='#000000')
    dropdown_text_color = models.CharField(max_length=7, default='#333333')
    dropdown_hover_background_color = models.CharField(max_length=7, default='#f2f2f2')
    dropdown_hover_text_color = models.CharField(max_length=7, default='#0056b3')
    nav_link_hover_color = models.CharField(max_length=7, default='#007bff')

    nav_link_hover_bg = models.CharField(max_length=7, default='#f5f5f5')

    pagination_background_color = models.CharField(max_length=7, default='#ffffff')
    pagination_text_color = models.CharField(max_length=7, default='#000000')
    # pagination_active_background_color = models.CharField(max_length=7, default='#007bff')
    # pagination_active_text_color = models.CharField(max_length=7, default='#ffffff')

    font_family = models.CharField(max_length=100, default='EB Garamond')

    # Kelime çıkarma için alan (virgülle ayrılmış)
    excluded_words = models.TextField(blank=True, default='', help_text='Virgülle ayrılmış çıkarılacak kelimeler')

    # Diğer renk alanlarını da ekleyin

    def __str__(self):
        return f"{self.user.username}'s profile"

class Question(models.Model):
    question_text = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)  # SEO-friendly URL
    subquestions = models.ManyToManyField('self', symmetrical=False, related_name='parent_questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    from_search = models.BooleanField(default=False)
    saveditem = GenericRelation('SavedItem')
    # parent_questions alanını kaldırdık
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    users = models.ManyToManyField(
        User, related_name='associated_questions', blank=True
    )
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.upvotes and self.upvotes < 0:
            raise ValidationError({'upvotes': 'Upvotes negatif olamaz'})
        if self.downvotes and self.downvotes < 0:
            raise ValidationError({'downvotes': 'Downvotes negatif olamaz'})

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            base_slug = slugify(self.question_text, allow_unicode=True)[:250]
            self.slug = base_slug
            # Eğer slug zaten varsa sonuna unique ID ekle
            counter = 1
            while Question.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question_text

    def has_subquestions(self):
        return self.subquestions.exists()

    def get_subquestions(self):
        return self.subquestions.all()

    def get_total_subquestions_count(self, visited=None):
        if visited is None:
            visited = set()
        if self.id in visited:
            return 0
        visited.add(self.id)
        count = 0
        for subquestion in self.subquestions.all():
            count += 1  # Doğrudan alt soruyu say
            count += subquestion.get_total_subquestions_count(visited)  # Alt soruların alt sorularını say
        return count

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),      # User's questions
            models.Index(fields=['-created_at']),              # Homepage questions list
            models.Index(fields=['question_text']),            # Search queries
        ]

class QuestionRelationship(models.Model):
    """
    Kullanıcı-bazlı parent-child soru ilişkisi.
    Her kullanıcının kendi harita bağlantıları var.
    """
    parent = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='child_relationships')
    child = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='parent_relationships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_relationships')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'child', 'user')
        indexes = [
            models.Index(fields=['parent', 'user']),
            models.Index(fields=['child', 'user']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.parent.question_text} → {self.child.question_text}"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    saveditem = GenericRelation('SavedItem')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.upvotes and self.upvotes < 0:
            raise ValidationError({'upvotes': 'Upvotes negatif olamaz'})
        if self.downvotes and self.downvotes < 0:
            raise ValidationError({'downvotes': 'Downvotes negatif olamaz'})

    class Meta:
        indexes = [
            models.Index(fields=['question', '-created_at']),  # Question detail page ordering
            models.Index(fields=['user', '-created_at']),      # User profile ordering
            models.Index(fields=['-created_at']),              # Homepage random items
        ]

    def __str__(self):
        return f"Answer to {self.question.question_text} by {self.user.username}"

class Message(models.Model):
    MESSAGE_TYPES = (
        ('normal', 'Normal'),
        ('mention', 'Mention'),
        ('system', 'System'),
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages'
    )
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='normal')

    # Mention için ilgili answer/question linki
    related_answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)
    related_question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username}: {self.body[:20]}"

class StartingQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='starting_questions')
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='starter_users'
    )

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text}"

class SavedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def save(self, *args, **kwargs):
        if not self.content_type and not self.object_id:
            if hasattr(self, 'question'):
                self.content_type = ContentType.objects.get_for_model(Question)
                self.object_id = self.question.id
            elif hasattr(self, 'answer'):
                self.content_type = ContentType.objects.get_for_model(Answer)
                self.object_id = self.answer.id
        super(SavedItem, self).save(*args, **kwargs)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()  # +1 or -1

    # New fields made non-nullable
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Remove old fields
    # question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True)
    # answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

class PinnedEntry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"PinnedEntry of {self.user.username}"

class Entry(models.Model):
    # Soru ve yanıtları temsil eden soyut bir model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class RandomSentence(models.Model):
    sentence = models.CharField(max_length=280)
    ignored_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='ignored_random_sentences'
    )
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.sentence[:50]
    
class Poll(models.Model):
    question_text = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_anonymous = models.BooleanField(default=True)
    # İlgili başlık soru modeliyle ilişki (eğer önceden Question modeli tanımlandıysa)
    related_question = models.ForeignKey('Question', on_delete=models.SET_NULL, null=True, blank=True)

    def is_active(self):
        return timezone.now() < self.end_date

    def duration_ok(self):
        # 1 yıldan uzun mu kontrol et
        return self.end_date <= (self.created_at + datetime.timedelta(days=365))

    def __str__(self):
        return self.question_text

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.poll.question_text} - {self.option_text}"

    @property
    def votes_count(self):
        return self.votes.count()

class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'option')

    def __str__(self):
        return f"{self.user.username} -> {self.option.option_text}"
    

class Definition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='definitions')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='definitions')
    definition_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.OneToOneField('Answer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.question.question_text} / {self.user.username}"
    
class Reference(models.Model):
    author_surname = models.CharField(max_length=100, verbose_name="Yazar Soyadı")
    author_name = models.CharField(max_length=100, verbose_name="Yazar Adı")
    year = models.PositiveIntegerField(verbose_name="Yıl")
    metin_ismi = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Metin İsmi"
    )
    rest = models.TextField(max_length=2000, verbose_name="Künyenin Kalanı")
    abbreviation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Kısaltma (Opsiyonel)"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='references')

    def __str__(self):
        # Çoklu yazarları düzgün formatla: "Dumézil, Georges; Ceminay, Cem"
        surnames = [s.strip() for s in self.author_surname.split(';') if s.strip()]
        names = [n.strip() for n in self.author_name.split(';') if n.strip()]

        authors = []
        for i in range(max(len(surnames), len(names))):
            surname = surnames[i] if i < len(surnames) else ''
            name = names[i] if i < len(names) else ''
            if surname or name:
                authors.append(f"{surname}, {name}".strip(', '))

        author_str = '; '.join(authors)
        metin = f", {self.metin_ismi}" if self.metin_ismi else ""
        return f"{author_str} ({self.year}){metin}"

    def get_usage_count(self):
        """
        Answer modelindeki answer_text alanında, hem (kaynak:REF_ID) 
        hem de (kaynak:REF_ID, sayfa:NUM) şeklinde geçen ifadeleri sayar.
        """
        from .models import Answer  # Lokal import döngüsel importları önlemek için.
        # Regex deseni: 
        # \(kaynak:REF_ID     -> literal olarak "(kaynak:REF_ID"
        # (?:,\s*sayfa:\d+)?   -> opsiyonel olarak ", sayfa:" ile başlayan ve sonrasında bir veya daha fazla rakam
        # \)                   -> kapanış parantezi
        pattern = re.compile(r'\(kaynak:{}(?:,\s*sayfa:\d+)?\)'.format(self.id))
        count = 0
        # İlk filtre, answer_text içerisinde "(kaynak:REF_ID" ifadesi geçiyorsa getiriyor
        answers = Answer.objects.filter(answer_text__icontains=f"(kaynak:{self.id}")
        for answer in answers:
            matches = pattern.findall(answer.answer_text)
            count += len(matches)
        return count

class IATResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_type = models.CharField(
        max_length=20,
        choices=[('gender', 'Cinsiyet'), ('ethnicity', 'Etnisite')]
    )
    dscore = models.FloatField()
    bias_side = models.CharField(max_length=20)
    errors = models.IntegerField()
    avg_rt = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.test_type} - {self.dscore:.2f}"


class Kenarda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kenardalar")
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True, blank=True, related_name="kenarda_taslaklar")  # <-- EKLENDİ!
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title or (self.question.question_text if self.question else '[Başlıksız]')}"

class CikisTesti(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cikis_testleri")
    title = models.CharField(max_length=200)
    cikis_dogrusu = models.PositiveIntegerField(null=True, blank=True)  # Sonradan ayarlanabilir
    created_at = models.DateTimeField(auto_now_add=True)

    def soru_sayisi(self):
        return self.sorular.count()
    
    def __str__(self):
        return self.title

class CikisTestiSoru(models.Model):
    test = models.ForeignKey(CikisTesti, on_delete=models.CASCADE, related_name="sorular")
    question_text = models.TextField()
    order = models.PositiveIntegerField(default=0)
    # Doğru şık (her zaman ilgili sorunun şıkları arasında olmalı)
    correct_option = models.ForeignKey(
        'CikisTestiSik',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )

    def __str__(self):
        return self.question_text

class CikisTestiSik(models.Model):
    soru = models.ForeignKey(CikisTestiSoru, on_delete=models.CASCADE, related_name="siklar")
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text[:40]
    

class CikisTestiResult(models.Model):
    test = models.ForeignKey(CikisTesti, on_delete=models.CASCADE, related_name="sonuclar")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    dogru_sayisi = models.PositiveIntegerField()
    toplam_soru = models.PositiveIntegerField()
    cikis_dogrusu_uydu = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.test.title} sonucu"


class DelphoiProphecy(models.Model):
    TYPE_CHOICES = (
        ('positive', 'Pozitif'),
        ('negative', 'Negatif'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='delphoi_prophecies')
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class DelphoiRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'requested_at', 'question')

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.name}"

    def get_usage_count(self):
        """Returns total usage count from answers and questions"""
        return self.answers.count() + self.questions.count()

    def get_recent_answers(self, limit=20):
        """Returns recent answers containing this hashtag"""
        return self.answers.select_related('user', 'question').order_by('-created_at')[:limit]

    class Meta:
        ordering = ['-created_at']

class HashtagUsage(models.Model):
    """Track hashtag usage in answers and questions"""
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name='usages')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, related_name='hashtags')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name='hashtags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['hashtag', '-created_at']),
        ]

    def __str__(self):
        if self.answer:
            return f"#{self.hashtag.name} in answer {self.answer.id}"
        return f"#{self.hashtag.name} in question {self.question.id}"


# ========== SIGNALS FOR MENTIONS AND HASHTAGS ==========

@receiver(post_save, sender=Answer)
def process_answer_mentions_and_hashtags(sender, instance, created, **kwargs):
    """
    Process mentions and hashtags when an answer is created or updated
    """
    from .utils import extract_mentions, send_mention_notifications, process_hashtags

    if created:
        # Extract and send mention notifications
        mentioned_usernames = extract_mentions(instance.answer_text)
        if mentioned_usernames:
            send_mention_notifications(instance, mentioned_usernames)

    # Process hashtags (both create and update)
    process_hashtags(answer=instance)


@receiver(post_save, sender=Question)
def process_question_hashtags(sender, instance, created, **kwargs):
    """
    Process hashtags when a question is created or updated
    """
    from .utils import process_hashtags
    process_hashtags(question=instance)


@receiver(post_delete, sender=Answer)
def cleanup_answer_hashtags(sender, instance, **kwargs):
    """
    Clean up hashtag usages when answer is deleted
    """
    HashtagUsage.objects.filter(answer=instance).delete()


@receiver(post_delete, sender=Question)
def cleanup_question_hashtags(sender, instance, **kwargs):
    """
    Clean up hashtag usages when question is deleted
    """
    HashtagUsage.objects.filter(question=instance).delete()


# ========== FOLLOW SYSTEM MODELS ==========

class QuestionFollow(models.Model):
    """Track users following specific questions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
        ordering = ['-followed_at']
        indexes = [
            models.Index(fields=['user', '-followed_at']),
            models.Index(fields=['question', '-followed_at']),
        ]

    def __str__(self):
        return f"{self.user.username} follows {self.question.question_text}"


class AnswerFollow(models.Model):
    """Track users following specific answers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_answers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')
        ordering = ['-followed_at']
        indexes = [
            models.Index(fields=['user', '-followed_at']),
            models.Index(fields=['answer', '-followed_at']),
        ]

    def __str__(self):
        return f"{self.user.username} follows answer {self.answer.id}"


# ========== NOTIFICATION SYSTEM ==========

class Notification(models.Model):
    """Unified notification system for all user notifications"""
    NOTIFICATION_TYPES = (
        ('mention', 'Mention'),                    # @username mention
        ('new_answer', 'New Answer'),              # New answer to followed question
        ('answer_update', 'Answer Update'),        # Update to followed answer
        ('question_update', 'Question Update'),    # Update to followed question
        ('new_subquestion', 'New Subquestion'),    # New subquestion to followed question
        ('followed_user_entry', 'Followed User Entry'),  # Entry from followed user
        ('system', 'System'),                      # System notifications
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()

    # Related objects (optional, depending on notification type)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    related_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['recipient', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient.username}"

    def mark_as_read(self):
        """Mark this notification as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    @classmethod
    def create_mention_notification(cls, recipient, sender, answer=None, question=None):
        """Create a mention notification"""
        if answer:
            message = f"{sender.username} seni bir yanıtta bahsetti: {answer.question.question_text}"
            return cls.objects.create(
                recipient=recipient,
                sender=sender,
                notification_type='mention',
                message=message,
                related_answer=answer,
                related_question=answer.question
            )
        elif question:
            message = f"{sender.username} seni bir başlıkta bahsetti: {question.question_text}"
            return cls.objects.create(
                recipient=recipient,
                sender=sender,
                notification_type='mention',
                message=message,
                related_question=question
            )

    @classmethod
    def create_new_answer_notification(cls, recipient, answer):
        """Create notification for new answer to followed question"""
        message = f"{answer.user.username} takip ettiğin başlığa yanıt verdi: {answer.question.question_text}"
        return cls.objects.create(
            recipient=recipient,
            sender=answer.user,
            notification_type='new_answer',
            message=message,
            related_answer=answer,
            related_question=answer.question
        )

    @classmethod
    def create_answer_update_notification(cls, recipient, answer):
        """Create notification for update to followed answer"""
        message = f"{answer.user.username} takip ettiğin yanıtı güncelledi"
        return cls.objects.create(
            recipient=recipient,
            sender=answer.user,
            notification_type='answer_update',
            message=message,
            related_answer=answer,
            related_question=answer.question
        )

    @classmethod
    def create_question_update_notification(cls, recipient, question):
        """Create notification for update to followed question"""
        message = f"{question.user.username} takip ettiğin başlığı güncelledi: {question.question_text}"
        return cls.objects.create(
            recipient=recipient,
            sender=question.user,
            notification_type='question_update',
            message=message,
            related_question=question
        )

    @classmethod
    def create_new_subquestion_notification(cls, recipient, subquestion, parent_question):
        """Create notification for new subquestion to followed question"""
        message = f"{subquestion.user.username} takip ettiğin başlığa alt soru ekledi: {subquestion.question_text}"
        return cls.objects.create(
            recipient=recipient,
            sender=subquestion.user,
            notification_type='new_subquestion',
            message=message,
            related_question=subquestion
        )

    @classmethod
    def create_followed_user_entry_notification(cls, recipient, answer):
        """Create notification for new entry from followed user"""
        message = f"{answer.user.username} yeni bir entry girdi: {answer.question.question_text}"
        return cls.objects.create(
            recipient=recipient,
            sender=answer.user,
            notification_type='followed_user_entry',
            message=message,
            related_answer=answer,
            related_question=answer.question
        )


# ========== SIGNALS FOR FOLLOW NOTIFICATIONS ==========

@receiver(post_save, sender=Answer)
def notify_question_followers_on_new_answer(sender, instance, created, **kwargs):
    """Notify followers when a new answer is added to a question they follow"""
    if created:
        # Get all users following this question
        followers = QuestionFollow.objects.filter(
            question=instance.question
        ).exclude(user=instance.user).select_related('user')

        # Create notifications for each follower
        for follow in followers:
            Notification.create_new_answer_notification(
                recipient=follow.user,
                answer=instance
            )
    else:
        # Answer was updated - notify answer followers
        followers = AnswerFollow.objects.filter(
            answer=instance
        ).exclude(user=instance.user).select_related('user')

        for follow in followers:
            Notification.create_answer_update_notification(
                recipient=follow.user,
                answer=instance
            )


@receiver(post_save, sender=Question)
def notify_question_followers_on_update(sender, instance, created, **kwargs):
    """Notify followers when a question is updated"""
    if not created:
        # Question was updated
        followers = QuestionFollow.objects.filter(
            question=instance
        ).exclude(user=instance.user).select_related('user')

        for follow in followers:
            Notification.create_question_update_notification(
                recipient=follow.user,
                question=instance
            )


@receiver(post_save, sender=Answer)
def notify_user_followers_on_new_entry(sender, instance, created, **kwargs):
    """Notify followers when a followed user posts a new entry"""
    if created:
        try:
            author_profile = instance.user.userprofile
            # Get all users following this author
            followers = author_profile.followers.all()

            for follower_profile in followers:
                Notification.create_followed_user_entry_notification(
                    recipient=follower_profile.user,
                    answer=instance
                )
        except UserProfile.DoesNotExist:
            pass


# ==================== RADYO SİSTEMİ ====================

class RadioProgram(models.Model):
    """
    Radyo programı modeli
    DJ'ler program oluşturabilir ve canlı yayın yapabilir
    """
    dj = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='radio_programs',
        verbose_name='DJ'
    )
    title = models.CharField(max_length=200, verbose_name='Program Başlığı')
    description = models.TextField(blank=True, verbose_name='Açıklama')
    start_time = models.DateTimeField(verbose_name='Başlangıç Zamanı')
    end_time = models.DateTimeField(verbose_name='Bitiş Zamanı')

    # Yayın durumu
    is_live = models.BooleanField(default=False, verbose_name='Canlı Yayında')
    is_finished = models.BooleanField(default=False, verbose_name='Tamamlandı')

    # Agora.io için benzersiz kanal adı
    agora_channel_name = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='Agora Kanal Adı'
    )

    # İstatistikler
    listener_count = models.PositiveIntegerField(default=0, verbose_name='Dinleyici Sayısı')
    max_listeners = models.PositiveIntegerField(default=0, verbose_name='Max Dinleyici')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme')

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Radyo Programı'
        verbose_name_plural = 'Radyo Programları'
        indexes = [
            models.Index(fields=['-start_time']),
            models.Index(fields=['is_live']),
        ]

    def __str__(self):
        return f"{self.title} - DJ: {self.dj.username}"

    def save(self, *args, **kwargs):
        # Agora kanal adı otomatik oluştur
        if not self.agora_channel_name:
            import uuid
            self.agora_channel_name = f"radio_{uuid.uuid4().hex[:12]}"
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError

        # Bitiş zamanı başlangıçtan önce olamaz
        if self.end_time <= self.start_time:
            raise ValidationError({
                'end_time': 'Bitiş zamanı başlangıç zamanından sonra olmalıdır.'
            })

        # Çakışan program kontrolü
        conflicts = RadioProgram.objects.filter(
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if conflicts.exists():
            conflict = conflicts.first()
            raise ValidationError(
                f'Bu saatlerde başka bir program var: {conflict.title} '
                f'({conflict.dj.username})'
            )

    @property
    def is_upcoming(self):
        """Program henüz başlamadı mı?"""
        return timezone.now() < self.start_time

    @property
    def is_active_time(self):
        """Şu an program saati mi?"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def status(self):
        """Program durumu"""
        if self.is_finished:
            return 'finished'
        elif self.is_live:
            return 'live'
        elif self.is_active_time:
            return 'ready'  # Saati geldi ama DJ başlatmamış
        elif self.is_upcoming:
            return 'upcoming'
        else:
            return 'past'

    @property
    def duration_minutes(self):
        """Program süresi (dakika)"""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)