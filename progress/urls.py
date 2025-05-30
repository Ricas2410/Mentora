from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.ProgressOverviewView.as_view(), name='overview'),
    path('level/<uuid:level_id>/', views.LevelProgressView.as_view(), name='level'),
    path('topic/<uuid:topic_id>/', views.TopicProgressView.as_view(), name='topic'),
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
    path('study-sessions/', views.StudySessionsView.as_view(), name='study_sessions'),
]
