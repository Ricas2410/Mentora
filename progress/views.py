from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import UserProgress, TopicProgress, StudySession
from subjects.models import Subject, Topic
from content.models import Quiz, Test


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

        # Enhanced subject progress data with levels
        enhanced_subjects = []
        for subject in subjects:
            # Get all class levels for this subject
            from subjects.models import ClassLevel
            class_levels = ClassLevel.objects.filter(
                subject=subject,
                is_active=True
            ).order_by('level_number')

            # Calculate overall subject progress
            all_subject_topics = Topic.objects.filter(class_level__subject=subject, is_active=True)
            completed_subject_topics = topic_progress.filter(topic__in=all_subject_topics, is_completed=True).count()
            total_subject_topics = all_subject_topics.count()
            subject_progress_percentage = (completed_subject_topics / total_subject_topics * 100) if total_subject_topics > 0 else 0

            # Build levels data
            levels = []
            for level in class_levels:
                level_topics = Topic.objects.filter(class_level=level, is_active=True)
                level_completed = topic_progress.filter(topic__in=level_topics, is_completed=True).count()
                level_total = level_topics.count()
                level_progress = (level_completed / level_total * 100) if level_total > 0 else 0

                # Determine level status
                is_completed = level_progress >= 100
                is_current = (level.level_number == current_class_level and not is_completed)

                levels.append({
                    'name': f"Grade {level.level_number} - {level.name}",
                    'progress_percentage': level_progress,
                    'is_completed': is_completed,
                    'is_current': is_current,
                    'url': f"/subjects/{subject.id}/levels/{level.id}/" if level_total > 0 else None
                })

            # Determine subject color based on name
            color_map = {
                'english': 'blue',
                'mathematics': 'green',
                'math': 'green',
                'science': 'purple',
                'social': 'orange',
                'history': 'red',
                'geography': 'teal',
                'art': 'pink',
                'music': 'indigo'
            }
            subject_color = 'blue'  # default
            for key, color in color_map.items():
                if key in subject.name.lower():
                    subject_color = color
                    break

            # Determine subject icon
            icon_map = {
                'english': '📚',
                'mathematics': '🔢',
                'math': '🔢',
                'science': '🔬',
                'social': '🌍',
                'history': '📜',
                'geography': '🗺️',
                'art': '🎨',
                'music': '🎵'
            }
            subject_icon = '📚'  # default
            for key, icon in icon_map.items():
                if key in subject.name.lower():
                    subject_icon = icon
                    break

            # Find current level URL
            current_level_url = None
            for level in levels:
                if level['is_current'] and level['url']:
                    current_level_url = level['url']
                    break

            enhanced_subjects.append({
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'progress_percentage': subject_progress_percentage,
                'color': subject_color,
                'icon': subject_icon,
                'levels': levels,
                'current_level_url': current_level_url
            })

        # Keep original subject_progress for backward compatibility
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
        quiz_attempts = Quiz.objects.filter(user=user)
        test_attempts = Test.objects.filter(user=user)

        total_quizzes = quiz_attempts.count()
        passed_quizzes = quiz_attempts.filter(percentage__gte=60).count()
        total_tests = test_attempts.count()
        passed_tests = test_attempts.filter(percentage__gte=60).count()

        avg_quiz_score = quiz_attempts.aggregate(avg=Avg('percentage'))['avg'] or 0
        avg_test_score = test_attempts.aggregate(avg=Avg('percentage'))['avg'] or 0

        # Study time stats
        total_study_time = StudySession.objects.filter(user=user).aggregate(
            total=Sum('duration')
        )['total'] or 0

        # Calculate study streak and week activity
        from datetime import datetime, timedelta
        today = timezone.now().date()

        # Calculate study streak (consecutive days with study sessions)
        study_streak = 0
        current_date = today
        while True:
            sessions_on_date = StudySession.objects.filter(
                user=user,
                started_at__date=current_date
            ).exists()

            if sessions_on_date:
                study_streak += 1
                current_date -= timedelta(days=1)
            else:
                break

            # Limit to reasonable streak calculation
            if study_streak > 365:
                break

        # Calculate this week's activity (last 7 days)
        week_activity = []
        week_study_days = 0
        for i in range(7):
            date = today - timedelta(days=6-i)
            has_sessions = StudySession.objects.filter(
                user=user,
                started_at__date=date
            ).exists()

            if has_sessions:
                week_study_days += 1

            week_activity.append({
                'date': date,
                'studied': has_sessions,
                'partial': False  # Could be enhanced to show partial study days
            })

        # Get recent achievements (last 5)
        recent_achievements = []
        # This would be populated from actual achievement data
        # For now, we'll leave it empty and the template will handle it

        context.update({
            'current_class_level': current_class_level,
            'subjects': enhanced_subjects,  # Use enhanced subjects with level data
            'subject_progress': subject_progress,  # Keep for backward compatibility
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
            # New variables for enhanced UI
            'study_streak': study_streak,
            'week_activity': week_activity,
            'week_study_days': week_study_days,
            'recent_achievements': recent_achievements,
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
        quiz_attempts = Quiz.objects.filter(user=user)
        test_attempts = Test.objects.filter(user=user)
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
                'earned_date': quiz_attempts.first().started_at,
                'category': 'learning',
                'icon': 'fas fa-question-circle'
            })

        # Perfect Score Achievement
        perfect_scores = quiz_attempts.filter(percentage=100).count() + test_attempts.filter(percentage=100).count()
        if perfect_scores > 0:
            achievements_earned += 1
            total_points += 50
            achievements.append({
                'title': 'Perfect Score',
                'description': 'Score 100% on any quiz or test',
                'points': 50,
                'earned': True,
                'earned_date': quiz_attempts.filter(percentage=100).first().started_at if quiz_attempts.filter(percentage=100).exists() else test_attempts.filter(percentage=100).first().started_at,
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
        passed_quizzes_count = quiz_attempts.filter(percentage__gte=60).count()
        if passed_quizzes_count >= 10:
            achievements_earned += 1
            total_points += 40
            achievements.append({
                'title': 'Quiz Master',
                'description': 'Pass 10 quizzes with 60% or higher',
                'points': 40,
                'earned': True,
                'earned_date': quiz_attempts.filter(percentage__gte=60)[9].started_at if quiz_attempts.filter(percentage__gte=60).count() >= 10 else None,
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
