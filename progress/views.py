from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import UserProgress, TopicProgress, StudySession
from subjects.models import Subject, ClassLevel, Topic
from content.models import Quiz, Test, QuizAttempt, TestAttempt


class ProgressOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's current class level
        current_class_level = user.current_class_level

        # Get all subjects for the user's current class level
        if current_class_level:
            subjects = Subject.objects.filter(
                classlevels__level_number=current_class_level,
                is_active=True
            ).distinct()
        else:
            subjects = Subject.objects.filter(is_active=True)[:3]  # Default to first 3 subjects

        # Calculate overall stats
        user_progress = UserProgress.objects.filter(user=user)
        topic_progress = TopicProgress.objects.filter(user=user)

        # Subject progress data
        subject_progress = []
        for subject in subjects:
            # Get topics for this subject at user's level
            if current_class_level:
                topics = Topic.objects.filter(
                    class_level__subject=subject,
                    class_level__level_number=current_class_level,
                    is_active=True
                )
            else:
                topics = Topic.objects.filter(
                    class_level__subject=subject,
                    is_active=True
                )[:5]  # Limit to 5 topics if no specific level

            total_topics = topics.count()
            completed_topics = topic_progress.filter(
                topic__in=topics,
                is_completed=True
            ).count()

            progress_percentage = (completed_topics / total_topics * 100) if total_topics > 0 else 0

            subject_progress.append({
                'subject': subject,
                'total_topics': total_topics,
                'completed_topics': completed_topics,
                'progress_percentage': round(progress_percentage),
                'topics': topics[:3]  # Show first 3 topics for preview
            })

        # Calculate quiz and test stats
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        test_attempts = TestAttempt.objects.filter(user=user)

        total_quizzes = quiz_attempts.count()
        passed_quizzes = quiz_attempts.filter(score__gte=60).count()
        total_tests = test_attempts.count()
        passed_tests = test_attempts.filter(score__gte=60).count()

        avg_quiz_score = quiz_attempts.aggregate(avg=Avg('score'))['avg'] or 0
        avg_test_score = test_attempts.aggregate(avg=Avg('score'))['avg'] or 0

        # Study time stats
        total_study_time = StudySession.objects.filter(user=user).aggregate(
            total=Sum('duration')
        )['total'] or 0

        context.update({
            'current_class_level': current_class_level,
            'subjects': subjects,
            'subject_progress': subject_progress,
            'subjects_enrolled': subjects.count(),
            'levels_completed': user_progress.filter(is_completed=True).count(),
            'total_quizzes': total_quizzes,
            'passed_quizzes': passed_quizzes,
            'quiz_pass_rate': (passed_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'test_pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'avg_quiz_score': round(avg_quiz_score, 1),
            'avg_test_score': round(avg_test_score, 1),
            'total_study_time_hours': round(total_study_time / 60, 1) if total_study_time else 0,
            'completed_topics': topic_progress.filter(is_completed=True).count(),
            'total_topics': topic_progress.count(),
        })

        return context


class LevelProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/level.html'


class TopicProgressView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/topic.html'


class AchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'progress/achievements.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Calculate achievement stats
        quiz_attempts = QuizAttempt.objects.filter(user=user)
        test_attempts = TestAttempt.objects.filter(user=user)
        topic_progress = TopicProgress.objects.filter(user=user)
        study_sessions = StudySession.objects.filter(user=user)

        # Achievement calculations
        achievements_earned = 0
        total_points = 0

        # Check various achievements
        achievements = []

        # First Quiz Achievement
        first_quiz = quiz_attempts.exists()
        if first_quiz:
            achievements_earned += 1
            total_points += 10
            achievements.append({
                'title': 'First Quiz',
                'description': 'Complete your very first quiz',
                'points': 10,
                'earned': True,
                'earned_date': quiz_attempts.first().created_at,
                'category': 'learning',
                'icon': 'fas fa-question-circle'
            })

        # Perfect Score Achievement
        perfect_scores = quiz_attempts.filter(score=100).count() + test_attempts.filter(score=100).count()
        if perfect_scores > 0:
            achievements_earned += 1
            total_points += 50
            achievements.append({
                'title': 'Perfect Score',
                'description': 'Score 100% on any quiz or test',
                'points': 50,
                'earned': True,
                'earned_date': quiz_attempts.filter(score=100).first().created_at if quiz_attempts.filter(score=100).exists() else test_attempts.filter(score=100).first().created_at,
                'category': 'learning',
                'icon': 'fas fa-crown'
            })

        # Level Complete Achievement
        completed_levels = topic_progress.filter(is_completed=True).count()
        if completed_levels >= 5:  # Completed 5 topics = level complete
            achievements_earned += 1
            total_points += 30
            achievements.append({
                'title': 'Level Complete',
                'description': 'Complete your first class level',
                'points': 30,
                'earned': True,
                'earned_date': topic_progress.filter(is_completed=True).first().completed_at,
                'category': 'progress',
                'icon': 'fas fa-graduation-cap'
            })

        # Study Streak Achievement (7 consecutive days)
        # Check if user has study sessions in last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_sessions = study_sessions.filter(started_at__gte=seven_days_ago)
        unique_days = recent_sessions.values('started_at__date').distinct().count()

        if unique_days >= 7:
            achievements_earned += 1
            total_points += 25
            achievements.append({
                'title': 'Study Streak',
                'description': 'Study for 7 consecutive days',
                'points': 25,
                'earned': True,
                'earned_date': recent_sessions.last().started_at,
                'category': 'progress',
                'icon': 'fas fa-fire'
            })

        # Quiz Master Achievement (10 quizzes passed)
        passed_quizzes = quiz_attempts.filter(score__gte=60).count()
        if passed_quizzes >= 10:
            achievements_earned += 1
            total_points += 40
            achievements.append({
                'title': 'Quiz Master',
                'description': 'Pass 10 quizzes with 60% or higher',
                'points': 40,
                'earned': True,
                'earned_date': quiz_attempts.filter(score__gte=60)[9].created_at if quiz_attempts.filter(score__gte=60).count() >= 10 else None,
                'category': 'learning',
                'icon': 'fas fa-brain'
            })

        # Calculate this month's achievements
        this_month = timezone.now().replace(day=1)
        this_month_achievements = [a for a in achievements if a['earned'] and a['earned_date'] and a['earned_date'] >= this_month]

        # Count rare achievements (50+ points)
        rare_achievements = [a for a in achievements if a['earned'] and a['points'] >= 50]

        context.update({
            'achievements': achievements,
            'achievements_earned': achievements_earned,
            'total_points': total_points,
            'this_month_achievements': len(this_month_achievements),
            'rare_achievements': len(rare_achievements),
        })

        return context


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
