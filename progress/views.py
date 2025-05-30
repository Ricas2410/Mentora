from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count
from .models import UserProgress, TopicProgress, StudySession


class ProgressOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/overview.html'


class LevelProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/level.html'


class TopicProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/topic.html'


class AchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/achievements.html'


class StudySessionsView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/study_sessions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get user's study sessions
        study_sessions = StudySession.objects.filter(
            user=self.request.user
        ).select_related('topic', 'topic__class_level', 'topic__class_level__subject').order_by('-started_at')

        # Calculate statistics
        total_sessions = study_sessions.count()
        total_study_time_minutes = study_sessions.aggregate(
            total=Sum('duration')
        )['total'] or 0
        total_study_time_hours = round(total_study_time_minutes / 60, 1) if total_study_time_minutes > 0 else 0

        avg_session_time = study_sessions.aggregate(
            avg=Avg('duration')
        )['avg'] or 0
        avg_session_time = round(avg_session_time) if avg_session_time else 0

        # Paginate sessions
        paginator = Paginator(study_sessions, 10)  # Show 10 sessions per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context.update({
            'study_sessions': page_obj,
            'total_sessions': total_sessions,
            'total_study_time': total_study_time_hours,
            'avg_session_time': avg_session_time,
        })

        return context
