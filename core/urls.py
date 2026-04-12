from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views.answer_page_views import add_answer, delete_answer, edit_answer, single_answer
from .views.answer_profile_views import get_root_questions, get_user_answers
from .views.answer_revision_views import answer_git_history, answer_live_preview, answer_revision_approve, answer_revision_reject, answer_suggest_edit, answer_suggestion_accept, answer_suggestion_detail, answer_suggestion_reject
from .views.auth_views import create_invitation, send_invitation, signup, user_login, user_logout
from .views.cikis_test_views import cikis_dogru_sik_sec, cikis_dogrusu_ayarla, cikis_sik_edit, cikis_sik_ekle, cikis_sonuc_sil, cikis_soru_edit, cikis_soru_ekle, cikis_soru_sil, cikis_test_coz, cikis_test_list, cikis_testi_coz, cikis_testi_create, cikis_testi_detail, cikis_testi_sil, cikis_testi_sonuc_list, cikis_testleri_list
from .views.collection_views import create_saved_collection, delete_saved_collection, saved_collections_home, saved_item_collection_options, update_saved_item_collections
from .views.definition_reference_views import create_definition, create_reference, delete_definition, delete_reference, edit_definition, edit_reference, get_all_definitions, get_references, get_user_definitions
from .views.delphoi_views import delphoi_home, delphoi_result
from .views.error_views import custom_400_view, custom_403_view, custom_404_view, custom_500_view, custom_502_view, debug_show_400, debug_show_403, debug_show_404, debug_show_500, debug_show_502
from .views.export_views import download_entries_docx, download_entries_json, download_entries_pdf, download_entries_xlsx, filter_answers
from .views.german_views import german_course_home, german_lesson_detail, german_level_test
from .views.hashtag_views import all_hashtags, hashtag_view, search_hashtags, trending_hashtags
from .views.iat_views import game_of_life, iat_result, iat_result_page, iat_start, iat_test
from .views.kenarda_views import kenarda_gonder, kenarda_list, kenarda_preview, kenarda_save, kenarda_sil
from .views.library_views import file_library, file_library_delete, file_library_list, file_library_search, upload_editor_image
from .views.message_views import check_new_messages, message_detail, message_list, send_message_from_answer, send_message_from_user
from .views.notification_views import follow_answer, follow_question, get_unread_notification_count, mark_all_notifications_read, mark_notification_read, notification_list, unfollow_answer, unfollow_question
from .views.online_chat_views import online_chat_messages
from .views.poll_views import create_poll, delete_poll, edit_poll, poll_detail, poll_popover_content, poll_question_redirect, polls_home, vote_poll, vote_poll_ajax
from .views.question_map_views import map_data_view, question_map, question_schema, question_schema_children, question_schema_content, question_schema_search
from .views.question_link_views import add_existing_subquestion, admin_merge_question, search_questions_for_linking, search_questions_for_merging, unlink_from_parent
from .views.question_page_views import add_question, add_question_from_search, add_starting_question, add_subquestion, bkz_view, delete_question, question_detail
from .views.radio_views import create_program, delete_program, dj_dashboard, edit_program, get_agora_token, program_detail, radio_chat_messages, radio_home, start_broadcast, stop_broadcast, update_listener_count
from .views.random_sentence_views import add_random_sentence, get_random_sentence, ignore_random_sentence, vote_random_sentence
from .views.report_views import report_content, report_content_ajax
from .views.search_views import load_more_questions, load_more_search_results, reference_search, search, search_suggestions, user_search
from .views.site_views import about, random_question_id, shuffle_questions, site_statistics, user_homepage
from .views.user_views import follow_user, get_user_questions, profile, unfollow_user, update_profile_photo, user_list, user_profile, user_settings
from .views.vote_save_views import get_saved_items, pin_entry, save_item, unpin_entry, vote

urlpatterns = [
    # Ana Sayfa
    path('', user_homepage, name='user_homepage'),

    # Debug-only: themed error pages preview (local dev only)
    # Note: must be above the catch-all question routes.
    *(
        [
            path('__error__/400/', debug_show_400, name='debug_error_400'),
            path('__error__/403/', debug_show_403, name='debug_error_403'),
            path('__error__/404/', debug_show_404, name='debug_error_404'),
            path('__error__/500/', debug_show_500, name='debug_error_500'),
            path('__error__/502/', debug_show_502, name='debug_error_502'),
        ]
        if not getattr(settings, 'IS_HOSTED', False)
        else []
    ),


    # Kullanıcı Kayıt ve Giriş
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # Kullanıcı Profili
    path('profile/update_photo/', update_profile_photo, name='update_profile_photo'),
    path('pin_entry/answer/<int:answer_id>/', pin_entry, name='pin_entry'),
    path('unpin_entry/', unpin_entry, name='unpin_entry'),
    path('profile/', profile, name='profile'),
    path('profile/<str:username>/follow/', follow_user, name='follow_user'),
    path('profile/<str:username>/unfollow/', unfollow_user, name='unfollow_user'),
    path('profile/<str:username>/', user_profile, name='user_profile'),

    # Soru İşlemleri
    path('add-question/', add_question, name='add_question'),

    # Yanıt İşlemleri
    path('answer/<int:answer_id>/edit/', edit_answer, name='edit_answer'),
    path('answer/<int:answer_id>/delete/', delete_answer, name='delete_answer'),
    path('answer/<int:answer_id>/history/', answer_git_history, name='answer_git_history'),
    path('answer/<int:answer_id>/suggest/', answer_suggest_edit, name='answer_suggest_edit'),
    path('answer/preview/', answer_live_preview, name='answer_live_preview'),
    path('answer/revision/<int:revision_id>/approve/', answer_revision_approve, name='answer_revision_approve'),
    path('answer/revision/<int:revision_id>/reject/', answer_revision_reject, name='answer_revision_reject'),
    path('answer/suggestion/<int:suggestion_id>/', answer_suggestion_detail, name='answer_suggestion_detail'),
    path('answer/suggestion/<int:suggestion_id>/accept/', answer_suggestion_accept, name='answer_suggestion_accept'),
    path('answer/suggestion/<int:suggestion_id>/reject/', answer_suggestion_reject, name='answer_suggestion_reject'),

    # Mesajlaşma URL'leri
    path('messages/', message_list, name='message_list'),
    path('messages/<str:username>/', message_detail, name='message_detail'),
    path('send_message/answer/<int:answer_id>/', send_message_from_answer, name='send_message_from_answer'),
    path('check_new_messages/', check_new_messages, name='check_new_messages'),
    path('send_message/user/<int:user_id>/', send_message_from_user, name='send_message_from_user'),
    path('online-chat/messages/', online_chat_messages, name='online_chat_messages'),

    # Arama
    path('search/', search, name='search'),
    path('search_suggestions/', search_suggestions, name='search_suggestions'),
    path('load_more_questions/', load_more_questions, name='load_more_questions'),
    path('load_more_search_results/', load_more_search_results, name='load_more_search_results'),
    path('reference-search/', reference_search, name='reference_search'),
    path('user-search/', user_search, name='user_search'),
    path('search-questions-for-linking/', search_questions_for_linking, name='search_questions_for_linking'),
    # Admin-only endpoint (must NOT be under /admin/ because it conflicts with Django admin URLs)
    path('merge/search-questions/', search_questions_for_merging, name='search_questions_for_merging'),

    # Kullanıcı Ayarları
    path('settings/', user_settings, name='user_settings'),

    # Diğer İşlemler
    path('about/', about, name='about'),
    path('files/', file_library, name='file_library'),
    path('files/search/', file_library_search, name='file_library_search'),
    path('files/list/', file_library_list, name='file_library_list'),
    path('files/<int:file_id>/delete/', file_library_delete, name='file_library_delete'),
    path('upload-editor-image/', upload_editor_image, name='upload_editor_image'),
    path('statistics/', site_statistics, name='site_statistics'),
    path('almanca/', german_course_home, name='german_course_home'),
    path('almanca/<slug:level_slug>/seviye-bitirme-testi/', german_level_test, name='german_level_test'),
    path('almanca/<slug:level_slug>/<slug:lesson_slug>/', german_lesson_detail, name='german_lesson_detail'),
    path('map/', question_map, name='question_map'),
    path('map-data/', map_data_view, name='map_data'),
    path('map/schema/', question_schema, name='question_schema'),
    path('map/schema/search/', question_schema_search, name='question_schema_search'),
    path('map/schema/<int:question_id>/children/', question_schema_children, name='question_schema_children'),
    path('map/schema/<int:question_id>/content/', question_schema_content, name='question_schema_content'),
    path('add-starting-question/', add_starting_question, name='add_starting_question'),
    path('add_question_from_search/', add_question_from_search, name='add_question_from_search'),
    path('bkz/<path:query>/', bkz_view, name='bkz'),
    path('games/game-of-life/', game_of_life, name='game_of_life'),
    # AJAX İşlemleri
    path('vote/', vote, name='vote'),
    path('save-item/', save_item, name='save_item'),
    path('users/', user_list, name='user_list'),
    path('create_invitation/', create_invitation, name='create_invitation'),
    path('send-invitation/', send_invitation, name='send_invitation'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='core/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'), name='password_change_done'),

    path('random_sentence/', get_random_sentence, name='get_random_sentence'),
    path('add_random_sentence/', add_random_sentence, name='add_random_sentence'),
    path('ignore_random_sentence/', ignore_random_sentence, name='ignore_random_sentence'),
    path('vote_random_sentence/', vote_random_sentence, name='vote_random_sentence'),

    # ANKETLER/POLL URL'LERİ (tamamı "polls/" prefixli)
    path('polls/', polls_home, name='polls_home'),
    path('polls/create/', create_poll, name='create_poll'),
    path('polls/<int:poll_id>/edit/', edit_poll, name='edit_poll'),
    path('polls/<int:poll_id>/delete/', delete_poll, name='delete_poll'),
    path('polls/<int:poll_id>/vote/<int:option_id>/', vote_poll, name='vote_poll'),
    path('polls/<int:poll_id>/question/', poll_question_redirect, name='poll_question_redirect'),
    path('polls/<int:poll_id>/popover/', poll_popover_content, name='poll_popover'),
    path('polls/<int:poll_id>/vote-ajax/', vote_poll_ajax, name='vote_poll_ajax'),
    path('polls/<int:poll_id>/', poll_detail, name='poll_detail'),

    # Tanımlar ve referanslar (diğer özel işlemler)
    path('create-definition/<path:slug>/', create_definition, name='create_definition'),
    path('get-user-definitions/', get_user_definitions, name='get_user_definitions'),
    path('definition/<int:definition_id>/edit/', edit_definition, name='edit_definition'),
    path('definition/<int:definition_id>/delete/', delete_definition, name='delete_definition'),
    path('get-all-definitions/', get_all_definitions, name='get_all_definitions'),
    path('create-reference/', create_reference, name='create_reference'),
    path('get-references/', get_references, name='get_references'),
    path('reference/<int:reference_id>/edit/', edit_reference, name='edit_reference'),
    path('reference/<int:reference_id>/delete/', delete_reference, name='delete_reference'),
    # path('profile/<str:username>/download_entries/', download_entries, name='download_entries'),
    path('profile/<str:username>/download_entries_json/', download_entries_json, name='download_entries_json'),
    path('profile/<str:username>/download_entries_xlsx/', download_entries_xlsx, name='download_entries_xlsx'),
    path('profile/<str:username>/download_entries_docx/', download_entries_docx, name='download_entries_docx'),
    path('profile/<str:username>/download_entries_pdf/', download_entries_pdf, name='download_entries_pdf'),
    path('question/<int:question_id>/filter_answers/', filter_answers, name='filter_answers'),

    # Aramalar
    path('get-user-questions/', get_user_questions, name='get_user_questions'),
    path('get-user-answers/', get_user_answers, name='get_user_answers'),
    path('get-root-questions/', get_root_questions, name='get_root_questions'),
    path('get-saved-items/', get_saved_items, name='get_saved_items'),
    path('collections/', saved_collections_home, name='saved_collections_home'),
    path('collections/options/', saved_item_collection_options, name='saved_item_collection_options'),
    path('collections/create/', create_saved_collection, name='create_saved_collection'),
    path('collections/<int:collection_id>/delete/', delete_saved_collection, name='delete_saved_collection'),
    path('collections/saved-item/<int:saved_item_id>/update/', update_saved_item_collections, name='update_saved_item_collections'),
    path('report-content/', report_content, name='report_content'),
    path('report-content/ajax/', report_content_ajax, name='report_content_ajax'),

    path('iat/', iat_start, name='iat_start'),
    path('iat/test/', iat_test, name='iat_test'),
    path('iat/result/page/', iat_result_page, name='iat_result_page'),
    path('iat/result/', iat_result, name='iat_result'),

    path("kenarda/save/", kenarda_save, name="kenarda_save"),
    path("kenarda/preview/", kenarda_preview, name="kenarda_preview"),
    path('kenarda/', kenarda_list, name='kenarda_list'),
    path('kenarda/sil/<int:pk>/', kenarda_sil, name='kenarda_sil'),
    path('kenarda/gonder/<int:pk>/', kenarda_gonder, name='kenarda_gonder'),

    path('cikis_testleri/', cikis_testleri_list, name='cikis_testleri_list'),
    path('cikis_testleri/olustur/', cikis_testi_create, name='cikis_testi_create'),
    path('cikis_testleri/<int:test_id>/', cikis_testi_detail, name='cikis_testi_detail'),
    path('cikis_testleri/<int:test_id>/soru_ekle/', cikis_soru_ekle, name='cikis_soru_ekle'),
    path('cikis_testleri/soru/<int:soru_id>/sik_ekle/', cikis_sik_ekle, name='cikis_sik_ekle'),
    path('cikis_testleri/soru/<int:soru_id>/dogru_sik/', cikis_dogru_sik_sec, name='cikis_dogru_sik_sec'),
    path('cikis_testleri/<int:test_id>/coz/', cikis_testi_coz, name='cikis_testi_coz'),
    path('cikis_testleri/<int:test_id>/sonuclar/', cikis_testi_sonuc_list, name='cikis_testi_sonuc_list'),
    path('cikis_testleri/<int:test_id>/dogru_ayarla/', cikis_dogrusu_ayarla, name='cikis_dogrusu_ayarla'),
    path('cikis-testleri/', cikis_test_list, name='cikis_test_list'),
    path('cikis-test/<int:test_id>/coz/', cikis_test_coz, name='cikis_test_coz'),
    path('cikis_testleri/sonuc/<int:sonuc_id>/sil/', cikis_sonuc_sil, name='cikis_sonuc_sil'),
    path('cikis_testleri/soru/<int:soru_id>/edit/', cikis_soru_edit, name='cikis_soru_edit'),
    path('cikis_testleri/soru/<int:soru_id>/sil/', cikis_soru_sil, name='cikis_soru_sil'),
    path('cikis_testi/<int:test_id>/sil/', cikis_testi_sil, name='cikis_testi_sil'),
    path('cikis_testleri/sik/<int:sik_id>/edit/', cikis_sik_edit, name='cikis_sik_edit'),

    path('random_question_id/', random_question_id, name='random_question_id'),#bunu sonra kullanacağız.
    path('shuffle_questions/', shuffle_questions, name='shuffle_questions'),

    path('delphoi/', delphoi_home, name='delphoi_home'),
    path('delphoi/result/', delphoi_result, name='delphoi_result'),

    # Hashtag URLs
    path('hashtag/<str:hashtag_name>/', hashtag_view, name='hashtag_view'),
    path('hashtags/trending/', trending_hashtags, name='trending_hashtags'),
    path('hashtags/all/', all_hashtags, name='all_hashtags'),
    path('hashtags/search/', search_hashtags, name='search_hashtags'),

    # Notification URLs
    path('notifications/', notification_list, name='notification_list'),
    path('notifications/<int:notification_id>/mark-read/', mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/unread-count/', get_unread_notification_count, name='get_unread_notification_count'),

    # Follow URLs
    path('question/<int:question_id>/follow/', follow_question, name='follow_question'),
    path('question/<int:question_id>/unfollow/', unfollow_question, name='unfollow_question'),
    path('answer/<int:answer_id>/follow/', follow_answer, name='follow_answer'),
    path('answer/<int:answer_id>/unfollow/', unfollow_answer, name='unfollow_answer'),

    # Radio URLs
    path('radio/', radio_home, name='radio_home'),
    path('radio/program/<int:program_id>/', program_detail, name='program_detail'),
    path('radio/dj/', dj_dashboard, name='dj_dashboard'),
    path('radio/dj/create/', create_program, name='create_program'),
    path('radio/dj/edit/<int:program_id>/', edit_program, name='edit_program'),
    path('radio/dj/delete/<int:program_id>/', delete_program, name='delete_program'),
    path('radio/dj/start/<int:program_id>/', start_broadcast, name='start_broadcast'),
    path('radio/dj/stop/<int:program_id>/', stop_broadcast, name='stop_broadcast'),
    path('radio/token/<int:program_id>/', get_agora_token, name='get_agora_token'),
    path('radio/listener-count/<int:program_id>/', update_listener_count, name='update_listener_count'),
    path('radio/chat/<int:program_id>/', radio_chat_messages, name='radio_chat_messages'),

    # SLUG-BASED QUESTION URLS (EN SONDA OLMALI - catch-all)
    # Örnek: /ozgurluk-nedir/ veya /yapılacaklar/ -> question detail
    # SPESİFİK pattern'lar ÖNCE gelmeli (single_answer, add-answer, etc.)
    path('<path:slug>/answer/<int:answer_id>/', single_answer, name='single_answer'),
    path('<path:slug>/add-answer/', add_answer, name='add_answer'),
    path('<path:slug>/delete/', delete_question, name='delete_question'),
    path('<path:slug>/add-subquestion/', add_subquestion, name='add_subquestion'),
    path('<path:slug>/add-as-subquestion/', add_existing_subquestion, name='add_existing_subquestion'),
    path('<path:slug>/admin-merge/', admin_merge_question, name='admin_merge_question'),
    path('<path:slug>/unlink-from-parent/<int:parent_id>/', unlink_from_parent, name='unlink_from_parent'),
    path('<path:slug>/filter_answers/', filter_answers, name='filter_answers'),
    # EN GENEL pattern EN SONDA (catch-all)
    path('<path:slug>/', question_detail, name='question_detail'),
]

# Custom error handlers
handler400 = 'core.views.error_views.custom_400_view'
handler403 = 'core.views.error_views.custom_403_view'
handler404 = 'core.views.error_views.custom_404_view'
handler500 = 'core.views.error_views.custom_500_view'
handler502 = 'core.views.error_views.custom_502_view'
