from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.AdminDashboardView.as_view(), name='dashboard'),

    # Content Management
    path('subjects/', views.ManageSubjectsView.as_view(), name='subjects'),
    path('subjects/create/', views.CreateSubjectView.as_view(), name='create_subject'),
    path('subjects/<uuid:subject_id>/edit/', views.EditSubjectView.as_view(), name='edit_subject'),
    path('subjects/<uuid:subject_id>/delete/', views.DeleteSubjectView.as_view(), name='delete_subject'),

    path('levels/', views.ManageLevelsView.as_view(), name='levels'),
    path('levels/create/', views.CreateLevelView.as_view(), name='create_level'),
    path('levels/<uuid:level_id>/edit/', views.EditLevelView.as_view(), name='edit_level'),
    path('levels/<uuid:level_id>/delete/', views.DeleteLevelView.as_view(), name='delete_level'),

    path('topics/', views.ManageTopicsView.as_view(), name='topics'),
    path('topics/create/', views.CreateTopicView.as_view(), name='create_topic'),
    path('topics/<uuid:topic_id>/edit/', views.EditTopicView.as_view(), name='edit_topic'),
    path('topics/<uuid:topic_id>/delete/', views.DeleteTopicView.as_view(), name='delete_topic'),

    # Question Management
    path('questions/', views.ManageQuestionsView.as_view(), name='questions'),
    path('questions/create/', views.CreateQuestionView.as_view(), name='create_question'),
    path('questions/<uuid:question_id>/edit/', views.EditQuestionView.as_view(), name='edit_question'),
    path('questions/<uuid:question_id>/delete/', views.DeleteQuestionView.as_view(), name='delete_question'),

    # CSV Import/Export
    path('import/', views.CSVImportView.as_view(), name='csv_import'),
    path('export/template/', views.DownloadTemplateView.as_view(), name='download_template'),

    # Import Logs
    path('logs/', views.ImportLogsView.as_view(), name='import_logs'),
    path('logs/<uuid:log_id>/', views.ImportLogDetailView.as_view(), name='import_log_detail'),
    path('logs/<uuid:log_id>/delete/', views.DeleteImportLogView.as_view(), name='delete_import_log'),

    # User Management
    path('users/', views.ManageUsersView.as_view(), name='users'),
    path('users/create/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<uuid:user_id>/edit/', views.EditUserView.as_view(), name='edit_user'),
    path('users/<uuid:user_id>/delete/', views.DeleteUserView.as_view(), name='delete_user'),

    # Reports & Analytics
    path('reports/', views.ReportsView.as_view(), name='reports'),

    # Settings
    path('settings/', views.SiteSettingsView.as_view(), name='settings'),

    # API endpoints for AJAX
    path('api/subjects/', views.SubjectsAPIView.as_view(), name='api_subjects'),
    path('api/levels/', views.LevelsAPIView.as_view(), name='api_levels'),
    path('api/topics/', views.TopicsAPIView.as_view(), name='api_topics'),
    path('api/questions/', views.QuestionsAPIView.as_view(), name='api_questions'),
]
