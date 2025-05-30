from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('study/<uuid:topic_id>/', views.StudyNotesView.as_view(), name='study_notes'),
    path('quiz/<uuid:topic_id>/', views.QuizView.as_view(), name='quiz'),
    path('quiz/<uuid:quiz_id>/take/', views.TakeQuizView.as_view(), name='take_quiz'),
    path('quiz/<uuid:quiz_id>/result/', views.QuizResultView.as_view(), name='quiz_result'),
    path('test/<uuid:topic_id>/', views.TestView.as_view(), name='test'),
    path('test/<uuid:test_id>/take/', views.TakeTestView.as_view(), name='take_test'),
    path('test/<uuid:test_id>/result/', views.TestResultView.as_view(), name='test_result'),
    path('exam/<uuid:level_id>/', views.ExamView.as_view(), name='exam'),
    path('exam/<uuid:level_id>/take/', views.TakeExamView.as_view(), name='take_exam'),
    path('exam/<uuid:exam_id>/result/', views.ExamResultView.as_view(), name='exam_result'),
    # API endpoints
    path('api/validate-answer/', views.validate_text_answer, name='validate_text_answer'),
    path('api/submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('api/submit-exam/', views.submit_exam, name='submit_exam'),
    path('api/next-learning-path/', views.get_next_learning_path, name='next_learning_path'),
]
