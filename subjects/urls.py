from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='list'),
    path('learn/', views.SimpleLearnView.as_view(), name='simple_learn'),
    path('quiz/', views.QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:grade_number>/<uuid:subject_id>/', views.QuizTopicsView.as_view(), name='quiz_topics'),

    # Improved URLs - redirect to user's current grade topics
    path('<uuid:subject_id>/', views.SubjectRedirectView.as_view(), name='subject_redirect'),
    path('<uuid:subject_id>/levels/', views.ClassLevelListView.as_view(), name='levels'),
    path('<uuid:subject_id>/levels/<uuid:level_id>/', views.ClassLevelDetailView.as_view(), name='level_detail'),
    path('<uuid:subject_id>/levels/<uuid:level_id>/topics/', views.TopicListView.as_view(), name='topics'),
    path('<uuid:subject_id>/levels/<uuid:level_id>/topics/<uuid:topic_id>/', views.TopicDetailView.as_view(), name='topic_detail'),

    # API endpoints
    path('api/subjects-by-level/<int:level_number>/', views.SubjectsByLevelAPIView.as_view(), name='api_subjects_by_level'),
    path('api/quiz-topics/<int:level_number>/<uuid:subject_id>/', views.QuizTopicsByLevelSubjectAPIView.as_view(), name='api_quiz_topics'),
    path('api/user-grade-subjects/<int:grade_number>/', views.UserGradeSubjectsAPIView.as_view(), name='api_user_grade_subjects'),
    path('api/quiz-topics/<int:grade_number>/<uuid:subject_id>/', views.QuizTopicsWithProgressAPIView.as_view(), name='api_quiz_topics_with_progress'),
    path('api/mark-note-read/<uuid:note_id>/', views.MarkNoteAsReadView.as_view(), name='api_mark_note_read'),
]
