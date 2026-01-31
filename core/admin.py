from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django import forms
from .models import IATResult
from django.contrib import admin


from core.models import (
    Invitation, UserProfile, Question, Answer,
    Poll, PollOption, PollVote, SavedItem, Vote, PinnedEntry,
    Entry, RandomSentence, Message, Definition, Reference,CikisTesti,
    CikisTestiSoru, CikisTestiSik, CikisTestiResult,DelphoiProphecy,
    QuestionFollow, AnswerFollow, Notification, RadioProgram, RadioChatMessage
)

# =============================================================================
# 1) Standart Admin Kaydı (Invitation, UserProfile, SavedItem, Vote, PinnedEntry, Entry, RandomSentence)
# =============================================================================
admin.site.register(Invitation)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "last_seen", "invitation_quota", "is_dj")
    ordering = ("-last_seen",)
    search_fields = ("user__username", "user__email")
admin.site.register(SavedItem)
admin.site.register(Vote)
admin.site.register(PinnedEntry)
admin.site.register(Entry)
admin.site.register(RandomSentence)

# =============================================================================
# 2) Kullanıcı Admin – Mesaj Gönderme, Grupların Gösterimi ve Filtrelenmesi
# =============================================================================

# Mesaj gönderme formu
class MassMessageForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.HiddenInput)
    message_body = forms.CharField(
        label="Mesajınız",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 60}),
        required=True
    )

# Custom UserAdmin: 
# - list_display’e "display_groups" ekleyip, kullanıcıya ait grupları virgülle gösteriyoruz.
# - list_filter’e "groups" ekleyerek filtreleme yapabiliyoruz.
# - Ayrıca, admin action ile seçili kullanıcılara mesaj gönderme işlevini de koruyoruz.
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('display_groups', 'last_seen',)
    list_filter = UserAdmin.list_filter + ('groups',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("userprofile")
    
    def display_groups(self, obj):
        return ", ".join(g.name for g in obj.groups.all())
    display_groups.short_description = "Gruplar"

    def last_seen(self, obj):
        profile = getattr(obj, "userprofile", None)
        return getattr(profile, "last_seen", None)
    last_seen.short_description = "Son aktif"
    last_seen.admin_order_field = "userprofile__last_seen"

    actions = ["send_message_to_selected_users"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send-messages/',
                self.admin_site.admin_view(self.send_messages_intermediate),
                name='send_messages_intermediate',
            )
        ]
        return custom_urls + urls

    def send_message_to_selected_users(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Hiç kullanıcı seçmediniz!", level=messages.WARNING)
            return
        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
        return redirect(f"send-messages/?ids={','.join(selected)}")

    send_message_to_selected_users.short_description = "Seçili kullanıcılara mesaj gönder"

    def send_messages_intermediate(self, request):
        from core.models import Message
        ids_param = request.GET.get('ids', '')
        if not ids_param:
            self.message_user(request, "Kullanıcı seçilmedi veya geçersiz ID.", level=messages.ERROR)
            return redirect("..")
        user_ids = ids_param.split(',')
        selected_users = User.objects.filter(pk__in=user_ids)
        if request.method == 'POST':
            form = MassMessageForm(request.POST)
            if form.is_valid():
                message_body = form.cleaned_data['message_body']
                admin_user = request.user
                count = 0
                for user in selected_users:
                    if user != admin_user:
                        Message.objects.create(
                            sender=admin_user,
                            recipient=user,
                            body=message_body
                        )
                        count += 1
                self.message_user(request, f"{count} kullanıcıya mesaj gönderildi.")
                return redirect("/admin/auth/user/")
        else:
            initial_data = {'_selected_action': ids_param}
            form = MassMessageForm(initial=initial_data)
        return render(request, 'admin/send_message_form.html', {
            'form': form,
            'selected_users': selected_users,
        })

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# =============================================================================
# 3) Grup Admin – Mesaj Gönderme, Üye Listesi (Inline) ve Üyelerin Yönetimi
# =============================================================================

# Inline: Kullanıcı-Group ilişkisini yönetmek için User.groups.through modelini kullanıyoruz.
class UserGroupInline(admin.TabularInline):
    model = User.groups.through
    extra = 0
    verbose_name = "Üye"
    verbose_name_plural = "Üyeler"

# Grup mesajı gönderme formu
class GroupMassMessageForm(forms.Form):
    selected_action = forms.CharField(widget=forms.HiddenInput)
    message_body = forms.CharField(
        label="Mesajınız",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 60}),
        required=True
    )

# Custom GroupAdmin: 
# - Grup listesinden seçili gruplara mesaj göndermek için admin action ekleniyor.
# - Değişim (change) sayfasında üye listesi inline olarak gösteriliyor, böylece üyeleri görüntüleyip çıkartabiliyoruz.
class CustomGroupAdmin(admin.ModelAdmin):
    actions = ["send_message_to_group"]
    inlines = [UserGroupInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'send-group-messages/',
                self.admin_site.admin_view(self.send_group_messages_intermediate),
                name='send_group_messages_intermediate',
            )
        ]
        return custom_urls + urls

    def send_message_to_group(self, request, queryset):
        if not queryset.exists():
            self.message_user(request, "Hiç grup seçmediniz!", level=messages.WARNING)
            return
        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
        return redirect(f"send-group-messages/?ids={','.join(selected)}")

    send_message_to_group.short_description = "Seçili gruplara mesaj gönder"

    def send_group_messages_intermediate(self, request):
        from core.models import Message
        ids_param = request.GET.get('ids', '')
        if not ids_param:
            self.message_user(request, "Grup seçilmedi veya geçersiz ID.", level=messages.ERROR)
            return redirect("..")
        group_ids = ids_param.split(',')
        selected_groups = Group.objects.filter(pk__in=group_ids)
        if request.method == "POST":
            form = GroupMassMessageForm(request.POST)
            if form.is_valid():
                message_body = form.cleaned_data["message_body"]
                users_set = set()
                for group in selected_groups:
                    for user in group.user_set.all():
                        users_set.add(user)
                count = 0
                for user in users_set:
                    Message.objects.create(
                        sender=request.user,
                        recipient=user,
                        body=message_body
                    )
                    count += 1
                self.message_user(request, f"{count} kullanıcıya mesaj gönderildi.")
                return redirect("/admin/auth/group/")
        else:
            initial_data = {'selected_action': ','.join(str(g.id) for g in selected_groups)}
            form = GroupMassMessageForm(initial=initial_data)
        return render(request, "admin/send_group_message.html", {
            "groups": selected_groups,
            "form": form,
            "title": "Seçili gruplara mesaj gönder"
        })

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# =============================================================================
# 4) Soru, Yanıt, Anket ve Referans Admin Kayıtları
# =============================================================================
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text', 'slug', 'user__username']
    list_display = ['id', 'question_text', 'user', 'created_at', 'slug']
    list_filter = ['created_at', 'user']
    list_display_links = ['id', 'question_text']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    ordering = ['-created_at']
    fields = ['question_text', 'slug', 'user', 'created_at', 'updated_at']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['answer_text', 'question__question_text']
    list_display = ['short_answer', 'question', 'user', 'created_at']
    list_filter = ['created_at', 'user']

    def short_answer(self, obj):
        return obj.answer_text[:50]
    short_answer.short_description = 'Yanıt Metni'

    def question_text(self, obj):
        return obj.question.question_text
    question_text.short_description = 'Soru Metni'

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'created_by', 'created_at', 'end_date', 'is_anonymous']
    search_fields = ['question_text', 'created_by__username']
    list_filter = ['created_at', 'is_anonymous']

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option_text']
    search_fields = ['poll__question_text', 'option_text']

@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'option', 'voted_at']
    search_fields = ['user__username', 'option__option_text']
    list_filter = ['voted_at']

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    search_fields = ['author_surname', 'author_name', 'year', 'rest', 'abbreviation']
    list_display = ['author_surname', 'author_name', 'year', 'abbreviation', 'short_rest']
    list_filter = ['year']

    def short_rest(self, obj):
        return (obj.rest[:50] + "...") if len(obj.rest) > 50 else obj.rest
    short_rest.short_description = "Ek Bilgiler (kısaltılmış)"

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0

@admin.register(Definition)
class DefinitionAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'created_at', 'get_answer']
    search_fields = ['definition_text', 'question__question_text', 'user__username']
    list_filter = ['created_at', 'user']

    def get_answer(self, obj):
        try:
            return obj.answer.answer_text if obj.answer else '-'
        except Answer.DoesNotExist:
            return '-'
    get_answer.short_description = 'Yanıt'


@admin.register(IATResult)
class IATResultAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "test_type", "dscore", "errors", "avg_rt", "created_at"]
    list_filter = ["test_type", "user"]
    search_fields = ["user__username"]


@admin.register(CikisTesti)
class CikisTestiAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at', 'cikis_dogrusu']
    search_fields = ['title', 'owner__username']

@admin.register(CikisTestiSoru)
class CikisTestiSoruAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'test', 'order']
    search_fields = ['question_text', 'test__title']

@admin.register(CikisTestiSik)
class CikisTestiSikAdmin(admin.ModelAdmin):
    list_display = ['text', 'soru']

@admin.register(CikisTestiResult)
class CikisTestiResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'user', 'dogru_sayisi', 'toplam_soru', 'completed_at']

@admin.register(DelphoiProphecy)
class DelphoiProphecyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'question', 'type', 'short_text', 'created_at']
    list_filter = ['type', 'created_at', 'question', 'user']
    search_fields = ['text', 'user__username', 'question__question_text']

    def short_text(self, obj):
        return obj.text[:60] + ('...' if len(obj.text) > 60 else '')
    short_text.short_description = "Kehanet"


# =============================================================================
# 5) Takip ve Bildirim Admin Kayıtları
# =============================================================================
@admin.register(QuestionFollow)
class QuestionFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'followed_at']
    list_filter = ['followed_at']
    search_fields = ['user__username', 'question__question_text']
    date_hierarchy = 'followed_at'


@admin.register(AnswerFollow)
class AnswerFollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'followed_at']
    list_filter = ['followed_at']
    search_fields = ['user__username', 'answer__answer_text']
    date_hierarchy = 'followed_at'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'sender', 'short_message', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'sender__username', 'message']
    date_hierarchy = 'created_at'

    def short_message(self, obj):
        return obj.message[:60] + ('...' if len(obj.message) > 60 else '')
    short_message.short_description = 'Mesaj'

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} bildirim okundu olarak işaretlendi.")
    mark_as_read.short_description = "Seçili bildirimleri okundu olarak işaretle"

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} bildirim okunmadı olarak işaretlendi.")
    mark_as_unread.short_description = "Seçili bildirimleri okunmadı olarak işaretle"


# =============================================================================
# 6) Radyo Programları Admin
# =============================================================================
@admin.register(RadioProgram)
class RadioProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'dj', 'start_time', 'end_time', 'status_display', 'is_live', 'listener_count', 'max_listeners']
    list_filter = ['is_live', 'is_finished', 'start_time', 'dj']
    search_fields = ['title', 'description', 'dj__username']
    readonly_fields = ['agora_channel_name', 'created_at', 'updated_at', 'listener_count', 'max_listeners']
    date_hierarchy = 'start_time'
    ordering = ['-start_time']

    fieldsets = (
        ('Program Bilgileri', {
            'fields': ('dj', 'title', 'description')
        }),
        ('Zaman', {
            'fields': ('start_time', 'end_time')
        }),
        ('Yayın Durumu', {
            'fields': ('is_live', 'is_finished')
        }),
        ('Teknik', {
            'fields': ('agora_channel_name',),
            'classes': ('collapse',)
        }),
        ('İstatistikler', {
            'fields': ('listener_count', 'max_listeners', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_display(self, obj):
        return obj.status
    status_display.short_description = 'Durum'

    actions = ['mark_as_finished', 'cancel_programs']

    def mark_as_finished(self, request, queryset):
        updated = queryset.update(is_finished=True, is_live=False)
        self.message_user(request, f"{updated} program tamamlandı olarak işaretlendi.")
    mark_as_finished.short_description = "Seçili programları tamamlandı olarak işaretle"

    def cancel_programs(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} program iptal edildi.")
    cancel_programs.short_description = "Seçili programları iptal et"


@admin.register(RadioChatMessage)
class RadioChatMessageAdmin(admin.ModelAdmin):
    list_display = ['program', 'user', 'short_body', 'created_at']
    list_filter = ['program', 'created_at']
    search_fields = ['program__title', 'user__username', 'body']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def short_body(self, obj):
        return obj.body[:60] + ('...' if len(obj.body) > 60 else '')
    short_body.short_description = 'Mesaj'
