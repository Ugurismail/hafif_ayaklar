from importlib import import_module
from types import SimpleNamespace

from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings


def lazy_view(module_path, attr_name):
    def _wrapped(*args, **kwargs):
        view = getattr(import_module(module_path), attr_name)
        return view(*args, **kwargs)

    _wrapped.__name__ = attr_name
    _wrapped.__qualname__ = attr_name
    _wrapped.__module__ = __name__
    return _wrapped


_LAZY_VIEW_MODULES = {
    "about": "misc_views",
    "add_answer": "answer_views",
    "add_existing_subquestion": "question_views",
    "add_question": "question_views",
    "add_question_from_search": "question_views",
    "add_random_sentence": "random_sentence_views",
    "add_starting_question": "question_views",
    "add_subquestion": "question_views",
    "admin_merge_question": "question_views",
    "all_hashtags": "hashtag_views",
    "answer_git_history": "answer_views",
    "answer_live_preview": "answer_views",
    "answer_revision_approve": "answer_views",
    "answer_revision_reject": "answer_views",
    "answer_suggest_edit": "answer_views",
    "answer_suggestion_accept": "answer_views",
    "answer_suggestion_detail": "answer_views",
    "answer_suggestion_reject": "answer_views",
    "bkz_view": "question_views",
    "check_new_messages": "message_views",
    "cikis_dogru_sik_sec": "cikis_test_views",
    "cikis_dogrusu_ayarla": "cikis_test_views",
    "cikis_sik_edit": "cikis_test_views",
    "cikis_sik_ekle": "cikis_test_views",
    "cikis_sonuc_sil": "cikis_test_views",
    "cikis_soru_edit": "cikis_test_views",
    "cikis_soru_ekle": "cikis_test_views",
    "cikis_soru_sil": "cikis_test_views",
    "cikis_test_coz": "cikis_test_views",
    "cikis_test_list": "cikis_test_views",
    "cikis_testi_coz": "cikis_test_views",
    "cikis_testi_create": "cikis_test_views",
    "cikis_testi_detail": "cikis_test_views",
    "cikis_testi_sil": "cikis_test_views",
    "cikis_testi_sonuc_list": "cikis_test_views",
    "cikis_testleri_list": "cikis_test_views",
    "create_definition": "definition_reference_views",
    "create_invitation": "auth_views",
    "create_poll": "poll_views",
    "create_program": "radio_views",
    "create_reference": "definition_reference_views",
    "custom_400_view": "misc_views",
    "custom_403_view": "misc_views",
    "custom_404_view": "misc_views",
    "custom_500_view": "misc_views",
    "custom_502_view": "misc_views",
    "debug_show_400": "misc_views",
    "debug_show_403": "misc_views",
    "debug_show_404": "misc_views",
    "debug_show_500": "misc_views",
    "debug_show_502": "misc_views",
    "delete_answer": "answer_views",
    "delete_definition": "definition_reference_views",
    "delete_program": "radio_views",
    "delete_question": "question_views",
    "delete_reference": "definition_reference_views",
    "delphoi_home": "delphoi_views",
    "delphoi_result": "delphoi_views",
    "dj_dashboard": "radio_views",
    "download_entries_docx": "misc_views",
    "download_entries_json": "misc_views",
    "download_entries_pdf": "misc_views",
    "download_entries_xlsx": "misc_views",
    "edit_answer": "answer_views",
    "edit_definition": "definition_reference_views",
    "edit_program": "radio_views",
    "edit_reference": "definition_reference_views",
    "file_library": "misc_views",
    "file_library_delete": "misc_views",
    "file_library_list": "misc_views",
    "file_library_search": "misc_views",
    "filter_answers": "misc_views",
    "follow_answer": "notification_views",
    "follow_question": "notification_views",
    "follow_user": "user_views",
    "game_of_life": "iat_views",
    "german_course_home": "german_views",
    "german_lesson_detail": "german_views",
    "german_level_test": "german_views",
    "get_agora_token": "radio_views",
    "get_all_definitions": "definition_reference_views",
    "get_random_sentence": "random_sentence_views",
    "get_references": "definition_reference_views",
    "get_root_questions": "answer_views",
    "get_saved_items": "vote_save_views",
    "get_unread_notification_count": "notification_views",
    "get_user_answers": "answer_views",
    "get_user_definitions": "definition_reference_views",
    "get_user_questions": "user_views",
    "hashtag_view": "hashtag_views",
    "iat_result": "iat_views",
    "iat_result_page": "iat_views",
    "iat_start": "iat_views",
    "iat_test": "iat_views",
    "ignore_random_sentence": "random_sentence_views",
    "kenarda_gonder": "kenarda_views",
    "kenarda_list": "kenarda_views",
    "kenarda_preview": "kenarda_views",
    "kenarda_save": "kenarda_views",
    "kenarda_sil": "kenarda_views",
    "load_more_questions": "misc_views",
    "load_more_search_results": "misc_views",
    "map_data_view": "question_views",
    "mark_all_notifications_read": "notification_views",
    "mark_notification_read": "notification_views",
    "memur_exam": "misc_views",
    "message_detail": "message_views",
    "message_list": "message_views",
    "notification_list": "notification_views",
    "pin_entry": "vote_save_views",
    "poll_detail": "poll_views",
    "poll_popover_content": "poll_views",
    "poll_question_redirect": "poll_views",
    "polls_home": "poll_views",
    "profile": "user_views",
    "program_detail": "radio_views",
    "question_detail": "question_views",
    "question_map": "question_views",
    "question_schema": "question_views",
    "question_schema_children": "question_views",
    "question_schema_content": "question_views",
    "question_schema_search": "question_views",
    "radio_chat_messages": "radio_views",
    "radio_home": "radio_views",
    "random_question_id": "misc_views",
    "reference_search": "misc_views",
    "save_item": "vote_save_views",
    "search": "misc_views",
    "search_hashtags": "hashtag_views",
    "search_questions_for_linking": "question_views",
    "search_questions_for_merging": "question_views",
    "search_suggestions": "misc_views",
    "send_invitation": "auth_views",
    "send_message_from_answer": "message_views",
    "send_message_from_user": "message_views",
    "shuffle_questions": "misc_views",
    "signup": "auth_views",
    "single_answer": "answer_views",
    "site_statistics": "misc_views",
    "start_broadcast": "radio_views",
    "stop_broadcast": "radio_views",
    "trending_hashtags": "hashtag_views",
    "unfollow_answer": "notification_views",
    "unfollow_question": "notification_views",
    "unfollow_user": "user_views",
    "unlink_from_parent": "question_views",
    "unpin_entry": "vote_save_views",
    "update_listener_count": "radio_views",
    "update_profile_photo": "user_views",
    "upload_editor_image": "misc_views",
    "user_homepage": "misc_views",
    "user_list": "user_views",
    "user_login": "auth_views",
    "user_logout": "auth_views",
    "user_profile": "user_views",
    "user_search": "misc_views",
    "user_settings": "user_views",
    "vote": "vote_save_views",
    "vote_poll": "poll_views",
    "vote_poll_ajax": "poll_views",
    "vote_random_sentence": "random_sentence_views"
}

views = SimpleNamespace(**{
    name: lazy_view(f"core.views.{module_name}", name)
    for name, module_name in _LAZY_VIEW_MODULES.items()
    if name != "map_data_view"
})
map_data_view = lazy_view("core.views.question_views", "map_data_view")

urlpatterns = [
    # Ana Sayfa
    path('', views.user_homepage, name='user_homepage'),

    # Debug-only: themed error pages preview (local dev only)
    # Note: must be above the catch-all question routes.
    *(
        [
            path('__error__/400/', views.debug_show_400, name='debug_error_400'),
            path('__error__/403/', views.debug_show_403, name='debug_error_403'),
            path('__error__/404/', views.debug_show_404, name='debug_error_404'),
            path('__error__/500/', views.debug_show_500, name='debug_error_500'),
            path('__error__/502/', views.debug_show_502, name='debug_error_502'),
        ]
        if not getattr(settings, 'IS_HOSTED', False)
        else []
    ),


    # Kullanıcı Kayıt ve Giriş
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Kullanıcı Profili
    path('profile/update_photo/', views.update_profile_photo, name='update_profile_photo'),
    path('pin_entry/answer/<int:answer_id>/', views.pin_entry, name='pin_entry'),
    path('unpin_entry/', views.unpin_entry, name='unpin_entry'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),

    # Soru İşlemleri
    path('add-question/', views.add_question, name='add_question'),

    # Yanıt İşlemleri
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('answer/<int:answer_id>/history/', views.answer_git_history, name='answer_git_history'),
    path('answer/<int:answer_id>/suggest/', views.answer_suggest_edit, name='answer_suggest_edit'),
    path('answer/preview/', views.answer_live_preview, name='answer_live_preview'),
    path('answer/revision/<int:revision_id>/approve/', views.answer_revision_approve, name='answer_revision_approve'),
    path('answer/revision/<int:revision_id>/reject/', views.answer_revision_reject, name='answer_revision_reject'),
    path('answer/suggestion/<int:suggestion_id>/', views.answer_suggestion_detail, name='answer_suggestion_detail'),
    path('answer/suggestion/<int:suggestion_id>/accept/', views.answer_suggestion_accept, name='answer_suggestion_accept'),
    path('answer/suggestion/<int:suggestion_id>/reject/', views.answer_suggestion_reject, name='answer_suggestion_reject'),

    # Mesajlaşma URL'leri
    path('messages/', views.message_list, name='message_list'),
    path('messages/<str:username>/', views.message_detail, name='message_detail'),
    path('send_message/answer/<int:answer_id>/', views.send_message_from_answer, name='send_message_from_answer'),
    path('check_new_messages/', views.check_new_messages, name='check_new_messages'),
    path('send_message/user/<int:user_id>/', views.send_message_from_user, name='send_message_from_user'),

    # Arama
    path('search/', views.search, name='search'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('load_more_questions/', views.load_more_questions, name='load_more_questions'),
    path('load_more_search_results/', views.load_more_search_results, name='load_more_search_results'),
    path('reference-search/', views.reference_search, name='reference_search'),
    path('user-search/', views.user_search, name='user_search'),
    path('search-questions-for-linking/', views.search_questions_for_linking, name='search_questions_for_linking'),
    # Admin-only endpoint (must NOT be under /admin/ because it conflicts with Django admin URLs)
    path('merge/search-questions/', views.search_questions_for_merging, name='search_questions_for_merging'),

    # Kullanıcı Ayarları
    path('settings/', views.user_settings, name='user_settings'),

    # Diğer İşlemler
    path('about/', views.about, name='about'),
    path('files/', views.file_library, name='file_library'),
    path('files/search/', views.file_library_search, name='file_library_search'),
    path('files/list/', views.file_library_list, name='file_library_list'),
    path('files/<int:file_id>/delete/', views.file_library_delete, name='file_library_delete'),
    path('upload-editor-image/', views.upload_editor_image, name='upload_editor_image'),
    path('statistics/', views.site_statistics, name='site_statistics'),
    path('almanca/', views.german_course_home, name='german_course_home'),
    path('almanca/<slug:level_slug>/seviye-bitirme-testi/', views.german_level_test, name='german_level_test'),
    path('almanca/<slug:level_slug>/<slug:lesson_slug>/', views.german_lesson_detail, name='german_lesson_detail'),
    path('map/', views.question_map, name='question_map'),
    path('map-data/', map_data_view, name='map_data'),
    path('map/schema/', views.question_schema, name='question_schema'),
    path('map/schema/search/', views.question_schema_search, name='question_schema_search'),
    path('map/schema/<int:question_id>/children/', views.question_schema_children, name='question_schema_children'),
    path('map/schema/<int:question_id>/content/', views.question_schema_content, name='question_schema_content'),
    path('add-starting-question/', views.add_starting_question, name='add_starting_question'),
    path('add_question_from_search/', views.add_question_from_search, name='add_question_from_search'),
    path('bkz/<path:query>/', views.bkz_view, name='bkz'),
    path('games/game-of-life/', views.game_of_life, name='game_of_life'),
    path('memur-sinavi/', views.memur_exam, name='memur_exam'),

    # AJAX İşlemleri
    path('vote/', views.vote, name='vote'),
    path('save-item/', views.save_item, name='save_item'),
    path('users/', views.user_list, name='user_list'),
    path('create_invitation/', views.create_invitation, name='create_invitation'),
    path('send-invitation/', views.send_invitation, name='send_invitation'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='core/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), name='password_change_done'),

    path('random_sentence/', views.get_random_sentence, name='get_random_sentence'),
    path('add_random_sentence/', views.add_random_sentence, name='add_random_sentence'),
    path('ignore_random_sentence/', views.ignore_random_sentence, name='ignore_random_sentence'),
    path('vote_random_sentence/', views.vote_random_sentence, name='vote_random_sentence'),

    # ANKETLER/POLL URL'LERİ (tamamı "polls/" prefixli)
    path('polls/', views.polls_home, name='polls_home'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/<int:poll_id>/vote/<int:option_id>/', views.vote_poll, name='vote_poll'),
    path('polls/<int:poll_id>/question/', views.poll_question_redirect, name='poll_question_redirect'),
    path('polls/<int:poll_id>/popover/', views.poll_popover_content, name='poll_popover'),
    path('polls/<int:poll_id>/vote-ajax/', views.vote_poll_ajax, name='vote_poll_ajax'),
    path('polls/<int:poll_id>/', views.poll_detail, name='poll_detail'),

    # Tanımlar ve referanslar (diğer özel işlemler)
    path('create-definition/<path:slug>/', views.create_definition, name='create_definition'),
    path('get-user-definitions/', views.get_user_definitions, name='get_user_definitions'),
    path('definition/<int:definition_id>/edit/', views.edit_definition, name='edit_definition'),
    path('definition/<int:definition_id>/delete/', views.delete_definition, name='delete_definition'),
    path('get-all-definitions/', views.get_all_definitions, name='get_all_definitions'),
    path('create-reference/', views.create_reference, name='create_reference'),
    path('get-references/', views.get_references, name='get_references'),
    path('reference/<int:reference_id>/edit/', views.edit_reference, name='edit_reference'),
    path('reference/<int:reference_id>/delete/', views.delete_reference, name='delete_reference'),
    # path('profile/<str:username>/download_entries/', views.download_entries, name='download_entries'),
    path('profile/<str:username>/download_entries_json/', views.download_entries_json, name='download_entries_json'),
    path('profile/<str:username>/download_entries_xlsx/', views.download_entries_xlsx, name='download_entries_xlsx'),
    path('profile/<str:username>/download_entries_docx/', views.download_entries_docx, name='download_entries_docx'),
    path('profile/<str:username>/download_entries_pdf/', views.download_entries_pdf, name='download_entries_pdf'),
    path('question/<int:question_id>/filter_answers/', views.filter_answers, name='filter_answers'),

    # Aramalar
    path('get-user-questions/', views.get_user_questions, name='get_user_questions'),
    path('get-user-answers/', views.get_user_answers, name='get_user_answers'),
    path('get-root-questions/', views.get_root_questions, name='get_root_questions'),
    path('get-saved-items/', views.get_saved_items, name='get_saved_items'),

    path('iat/', views.iat_start, name='iat_start'),
    path('iat/test/', views.iat_test, name='iat_test'),
    path('iat/result/page/', views.iat_result_page, name='iat_result_page'),
    path('iat/result/', views.iat_result, name='iat_result'),

    path("kenarda/save/", views.kenarda_save, name="kenarda_save"),
    path("kenarda/preview/", views.kenarda_preview, name="kenarda_preview"),
    path('kenarda/', views.kenarda_list, name='kenarda_list'),
    path('kenarda/sil/<int:pk>/', views.kenarda_sil, name='kenarda_sil'),
    path('kenarda/gonder/<int:pk>/', views.kenarda_gonder, name='kenarda_gonder'),

    path('cikis_testleri/', views.cikis_testleri_list, name='cikis_testleri_list'),
    path('cikis_testleri/olustur/', views.cikis_testi_create, name='cikis_testi_create'),
    path('cikis_testleri/<int:test_id>/', views.cikis_testi_detail, name='cikis_testi_detail'),
    path('cikis_testleri/<int:test_id>/soru_ekle/', views.cikis_soru_ekle, name='cikis_soru_ekle'),
    path('cikis_testleri/soru/<int:soru_id>/sik_ekle/', views.cikis_sik_ekle, name='cikis_sik_ekle'),
    path('cikis_testleri/soru/<int:soru_id>/dogru_sik/', views.cikis_dogru_sik_sec, name='cikis_dogru_sik_sec'),
    path('cikis_testleri/<int:test_id>/coz/', views.cikis_testi_coz, name='cikis_testi_coz'),
    path('cikis_testleri/<int:test_id>/sonuclar/', views.cikis_testi_sonuc_list, name='cikis_testi_sonuc_list'),
    path('cikis_testleri/<int:test_id>/dogru_ayarla/', views.cikis_dogrusu_ayarla, name='cikis_dogrusu_ayarla'),
    path('cikis-testleri/', views.cikis_test_list, name='cikis_test_list'),
    path('cikis-test/<int:test_id>/coz/', views.cikis_test_coz, name='cikis_test_coz'),
    path('cikis_testleri/sonuc/<int:sonuc_id>/sil/', views.cikis_sonuc_sil, name='cikis_sonuc_sil'),
    path('cikis_testleri/soru/<int:soru_id>/edit/', views.cikis_soru_edit, name='cikis_soru_edit'),
    path('cikis_testleri/soru/<int:soru_id>/sil/', views.cikis_soru_sil, name='cikis_soru_sil'),
    path('cikis_testi/<int:test_id>/sil/', views.cikis_testi_sil, name='cikis_testi_sil'),
    path('cikis_testleri/sik/<int:sik_id>/edit/', views.cikis_sik_edit, name='cikis_sik_edit'),

    path('random_question_id/', views.random_question_id, name='random_question_id'),#bunu sonra kullanacağız.
    path('shuffle_questions/', views.shuffle_questions, name='shuffle_questions'),

    path('delphoi/', views.delphoi_home, name='delphoi_home'),
    path('delphoi/result/', views.delphoi_result, name='delphoi_result'),

    # Hashtag URLs
    path('hashtag/<str:hashtag_name>/', views.hashtag_view, name='hashtag_view'),
    path('hashtags/trending/', views.trending_hashtags, name='trending_hashtags'),
    path('hashtags/all/', views.all_hashtags, name='all_hashtags'),
    path('hashtags/search/', views.search_hashtags, name='search_hashtags'),

    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/unread-count/', views.get_unread_notification_count, name='get_unread_notification_count'),

    # Follow URLs
    path('question/<int:question_id>/follow/', views.follow_question, name='follow_question'),
    path('question/<int:question_id>/unfollow/', views.unfollow_question, name='unfollow_question'),
    path('answer/<int:answer_id>/follow/', views.follow_answer, name='follow_answer'),
    path('answer/<int:answer_id>/unfollow/', views.unfollow_answer, name='unfollow_answer'),

    # Radio URLs
    path('radio/', views.radio_home, name='radio_home'),
    path('radio/program/<int:program_id>/', views.program_detail, name='program_detail'),
    path('radio/dj/', views.dj_dashboard, name='dj_dashboard'),
    path('radio/dj/create/', views.create_program, name='create_program'),
    path('radio/dj/edit/<int:program_id>/', views.edit_program, name='edit_program'),
    path('radio/dj/delete/<int:program_id>/', views.delete_program, name='delete_program'),
    path('radio/dj/start/<int:program_id>/', views.start_broadcast, name='start_broadcast'),
    path('radio/dj/stop/<int:program_id>/', views.stop_broadcast, name='stop_broadcast'),
    path('radio/token/<int:program_id>/', views.get_agora_token, name='get_agora_token'),
    path('radio/listener-count/<int:program_id>/', views.update_listener_count, name='update_listener_count'),
    path('radio/chat/<int:program_id>/', views.radio_chat_messages, name='radio_chat_messages'),

    # SLUG-BASED QUESTION URLS (EN SONDA OLMALI - catch-all)
    # Örnek: /ozgurluk-nedir/ veya /yapılacaklar/ -> question detail
    # SPESİFİK pattern'lar ÖNCE gelmeli (single_answer, add-answer, etc.)
    path('<path:slug>/answer/<int:answer_id>/', views.single_answer, name='single_answer'),
    path('<path:slug>/add-answer/', views.add_answer, name='add_answer'),
    path('<path:slug>/delete/', views.delete_question, name='delete_question'),
    path('<path:slug>/add-subquestion/', views.add_subquestion, name='add_subquestion'),
    path('<path:slug>/add-as-subquestion/', views.add_existing_subquestion, name='add_existing_subquestion'),
    path('<path:slug>/admin-merge/', views.admin_merge_question, name='admin_merge_question'),
    path('<path:slug>/unlink-from-parent/<int:parent_id>/', views.unlink_from_parent, name='unlink_from_parent'),
    path('<path:slug>/filter_answers/', views.filter_answers, name='filter_answers'),
    # EN GENEL pattern EN SONDA (catch-all)
    path('<path:slug>/', views.question_detail, name='question_detail'),
]

# Custom error handlers
handler400 = 'core.views.misc_views.custom_400_view'
handler403 = 'core.views.misc_views.custom_403_view'
handler404 = 'core.views.misc_views.custom_404_view'
handler500 = 'core.views.misc_views.custom_500_view'
handler502 = 'core.views.custom_502_view'
