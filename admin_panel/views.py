import csv
import io
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View, ListView, DetailView
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q, Min
from django.db import models
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote, Quiz
from users.models import User
from progress.models import UserProgress
from analytics.models import PageVisit, UserActivity, SystemPerformanceMetrics
from analytics.utils import business_intelligence
from .models import SiteSettings, AdminActivity
from core.models import CSVImportLog
import os
import re
from difflib import SequenceMatcher
from collections import defaultdict

# Optional import for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
from .forms import (
    SiteSettingsForm, SubjectForm, ClassLevelForm, TopicForm,
    QuestionForm, AnswerChoiceFormSet,
    CSVImportForm, UserEditForm
)


class AdminLoginView(View):
    """Custom admin login view"""
    template_name = 'admin_panel/login.html'

    def get(self, request):
        # If user is already logged in and is admin, redirect to dashboard
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return redirect('admin_panel:dashboard')

        # If user is logged in but not admin, show access denied
        if request.user.is_authenticated:
            return render(request, 'admin_panel/access_denied.html')

        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')

        if not username or not password:
            messages.error(request, 'Please enter both username/email and password.')
            return render(request, self.template_name)

        # Try to authenticate with username or email
        user = authenticate(request, username=username, password=password)

        if not user:
            # Try with email if username failed
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            if user.is_active:
                # Check if user is admin
                if user.is_staff or user.is_superuser:
                    login(request, user)

                    # Set session expiry
                    if not remember_me:
                        request.session.set_expiry(0)  # Browser close
                    else:
                        request.session.set_expiry(1209600)  # 2 weeks

                    messages.success(request, f'Welcome to admin panel, {user.first_name}!')
                    return redirect('admin_panel:dashboard')
                else:
                    messages.error(request, 'You do not have admin privileges to access this panel.')
                    return render(request, 'admin_panel/access_denied.html')
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid username/email or password.')

        return render(request, self.template_name)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to ensure only admin users can access admin views"""
    login_url = '/my-admin/login/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('admin_panel:login')
        else:
            return render(self.request, 'admin_panel/access_denied.html')


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    """Main admin dashboard view"""
    template_name = 'admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get statistics
        total_users = User.objects.count()
        total_questions = Question.objects.count()
        total_quizzes = Quiz.objects.count()

        # Calculate date ranges
        today = timezone.now().date()
        this_month = today.replace(day=1)

        # User stats
        new_users_this_month = User.objects.filter(date_joined__gte=this_month).count()

        # Question stats
        active_questions = Question.objects.filter(is_active=True).count()

        # Quiz stats
        quizzes_today = Quiz.objects.filter(started_at__date=today).count()
        avg_score = Quiz.objects.filter(is_completed=True).aggregate(
            avg=Avg('percentage')
        )['avg'] or 0

        # Pass rate
        passed_quizzes = Quiz.objects.filter(is_completed=True, percentage__gte=70).count()
        completed_quizzes = Quiz.objects.filter(is_completed=True).count()
        pass_rate = (passed_quizzes / completed_quizzes * 100) if completed_quizzes > 0 else 0

        context['stats'] = {
            'total_users': total_users,
            'new_users_this_month': new_users_this_month,
            'total_questions': total_questions,
            'active_questions': active_questions,
            'total_quizzes': total_quizzes,
            'quizzes_today': quizzes_today,
            'avg_score': round(avg_score, 1),
            'pass_rate': round(pass_rate, 1),
        }

        # Content statistics
        subjects_count = Subject.objects.count()
        levels_count = ClassLevel.objects.count()
        topics_count = Topic.objects.count()
        materials_count = StudyNote.objects.count()

        max_count = max(subjects_count, levels_count, topics_count, total_questions, materials_count) or 1

        context['content_stats'] = {
            'subjects': subjects_count,
            'levels': levels_count,
            'topics': topics_count,
            'questions': total_questions,
            'materials': materials_count,
            'levels_percentage': (levels_count / max_count) * 100,
            'topics_percentage': (topics_count / max_count) * 100,
            'questions_percentage': (total_questions / max_count) * 100,
            'materials_percentage': (materials_count / max_count) * 100,
        }

        # Learning progress by grade (for the new dashboard)
        grade_progress = []
        for grade_num in range(1, 13):  # Grades 1-12
            # Count active users in this grade
            active_users = User.objects.filter(
                current_class_level=grade_num,
                is_active=True
            ).count()

            if active_users > 0:
                # Calculate average progress for this grade
                grade_subjects = Subject.objects.filter(
                    classlevels__level_number=grade_num,
                    is_active=True
                ).distinct()

                total_progress = 0
                progress_count = 0

                for subject in grade_subjects:
                    try:
                        class_level = ClassLevel.objects.get(
                            subject=subject,
                            level_number=grade_num,
                            is_active=True
                        )

                        # Get average progress for this subject in this grade
                        # Calculate completion percentage manually since it's a property
                        user_progresses = UserProgress.objects.filter(class_level=class_level)
                        if user_progresses.exists():
                            total_percentage = 0
                            count = 0
                            for up in user_progresses:
                                if up.total_topics > 0:
                                    percentage = (up.topics_completed / up.total_topics) * 100
                                    total_percentage += percentage
                                    count += 1
                            subject_progress = total_percentage / count if count > 0 else 0
                        else:
                            subject_progress = 0

                        total_progress += subject_progress
                        progress_count += 1

                    except ClassLevel.DoesNotExist:
                        continue

                avg_progress = (total_progress / progress_count) if progress_count > 0 else 0

                grade_progress.append({
                    'level_number': grade_num,
                    'active_users': active_users,
                    'avg_progress': round(avg_progress, 1)
                })

        context['grade_progress'] = grade_progress

        # Site settings
        context['settings'] = SiteSettings.get_settings()

        return context


class ManageSubjectsView(AdminRequiredMixin, TemplateView):
    """View for managing subjects by class level"""
    template_name = 'admin_panel/subjects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get selected class level
        selected_class_id = self.request.GET.get('class_level')

        # Get all class levels for the dropdown
        context['class_levels'] = ClassLevel.objects.select_related('subject').order_by('level_number', 'name')

        # If a class is selected, get subjects for that class
        if selected_class_id:
            try:
                selected_class = ClassLevel.objects.get(id=selected_class_id)
                context['selected_class'] = selected_class

                # Get subjects that have this class level
                subjects = Subject.objects.filter(
                    classlevels__id=selected_class_id
                ).annotate(
                    topics_count=Count('classlevels__topics', filter=Q(classlevels__id=selected_class_id)),
                    questions_count=Count('classlevels__topics__questions', filter=Q(classlevels__id=selected_class_id))
                ).order_by('order', 'name')

                context['subjects'] = subjects
                context['show_subjects'] = True

            except ClassLevel.DoesNotExist:
                context['error'] = 'Selected class level not found'
        else:
            # Show all subjects grouped by class level
            subjects = Subject.objects.annotate(
                levels_count=Count('classlevels'),
                topics_count=Count('classlevels__topics'),
                questions_count=Count('classlevels__topics__questions')
            ).order_by('order', 'name')

            context['subjects'] = subjects
            context['show_subjects'] = False

        context['current_filters'] = {
            'class_level': selected_class_id,
        }

        return context


class CreateSubjectView(AdminRequiredMixin, CreateView):
    """View for creating new subjects"""
    model = Subject
    form_class = SubjectForm
    template_name = 'admin_panel/create_subject.html'
    success_url = reverse_lazy('admin_panel:subjects')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='CREATE_SUBJECT',
            description=f'Created subject: {self.object.name}',
            model_name='Subject',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Subject "{self.object.name}" created successfully!')
        return response

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)


class EditSubjectView(AdminRequiredMixin, UpdateView):
    """View for editing subjects"""
    model = Subject
    form_class = SubjectForm
    template_name = 'admin_panel/edit_subject.html'
    success_url = reverse_lazy('admin_panel:subjects')
    pk_url_kwarg = 'subject_id'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='UPDATE_SUBJECT',
            description=f'Updated subject: {self.object.name}',
            model_name='Subject',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Subject "{self.object.name}" updated successfully!')
        return response

    def form_invalid(self, form):
        """Handle form validation errors"""
        messages.error(self.request, 'Please correct the errors below and try again.')
        return super().form_invalid(form)


class DeleteSubjectView(AdminRequiredMixin, DeleteView):
    """View for deleting subjects"""
    model = Subject
    success_url = reverse_lazy('admin_panel:subjects')
    pk_url_kwarg = 'subject_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        subject_name = self.object.name

        # Log activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DELETE_SUBJECT',
            description=f'Deleted subject: {subject_name}',
            model_name='Subject',
            object_id=str(self.object.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'Subject "{subject_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ManageLevelsView(AdminRequiredMixin, TemplateView):
    """View for managing class levels"""
    template_name = 'admin_panel/levels.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all levels with related data
        levels = ClassLevel.objects.select_related('subject').annotate(
            topics_count=Count('topics'),
            questions_count=Count('topics__questions')
        ).order_by('subject__name', 'level_number')

        # Pagination
        paginator = Paginator(levels, 10)
        page_number = self.request.GET.get('page')
        context['levels'] = paginator.get_page(page_number)

        return context


class CreateLevelView(AdminRequiredMixin, CreateView):
    """View for creating new class levels"""
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'admin_panel/create_level.html'
    success_url = reverse_lazy('admin_panel:levels')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='CREATE_LEVEL',
            description=f'Created level: {self.object.name}',
            model_name='ClassLevel',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Level "{self.object.name}" created successfully!')
        return response


class ManageTopicsView(AdminRequiredMixin, TemplateView):
    """View for managing topics"""
    template_name = 'admin_panel/topics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get hierarchical filter parameters
        class_filter = self.request.GET.get('class_level')
        subject_filter = self.request.GET.get('subject')
        search_query = self.request.GET.get('search')

        # Start with all topics
        topics = Topic.objects.select_related('class_level__subject').annotate(
            questions_count=Count('questions')
        )

        # Apply hierarchical filters
        if class_filter:
            # class_filter contains level_number, not ID
            topics = topics.filter(class_level__level_number=class_filter)
        if subject_filter:
            topics = topics.filter(class_level__subject_id=subject_filter)
        if search_query:
            topics = topics.filter(title__icontains=search_query)

        # Order by class level, then subject, then order
        topics = topics.order_by('class_level__level_number', 'class_level__subject__name', 'order')

        # Pagination
        paginator = Paginator(topics, 10)
        page_number = self.request.GET.get('page')
        context['topics'] = paginator.get_page(page_number)

        # Get hierarchical filter options - distinct grade levels only
        # Group by level_number to avoid duplicates across subjects
        class_levels_raw = ClassLevel.objects.filter(is_active=True).values(
            'level_number'
        ).annotate(
            name=models.Min('name')  # Take the first name for this level
        ).order_by('level_number')

        # Convert to a list of objects that the template can use
        context['class_levels'] = [
            {
                'id': level['level_number'],  # Use level_number as ID for filtering
                'name': f"Grade {level['level_number']}",  # Standardize the name
                'level_number': level['level_number']
            }
            for level in class_levels_raw
        ]

        # Get subjects based on selected class level
        if class_filter:
            context['subjects'] = Subject.objects.filter(
                classlevels__level_number=class_filter,
                is_active=True
            ).distinct().order_by('name')
        else:
            context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')

        # Current filter values
        context['current_filters'] = {
            'class_level': class_filter,
            'subject': subject_filter,
            'search': search_query,
        }

        return context


class ManageQuestionsView(AdminRequiredMixin, TemplateView):
    """View for managing questions with hierarchical filtering"""
    template_name = 'admin_panel/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get hierarchical filter parameters
        class_filter = self.request.GET.get('class_level')
        subject_filter = self.request.GET.get('subject')
        topic_filter = self.request.GET.get('topic')
        type_filter = self.request.GET.get('type')
        search_query = self.request.GET.get('search')

        # Start with all questions
        questions = Question.objects.select_related('topic__class_level__subject').annotate(
            choices_count=Count('answer_choices')
        )

        # Apply hierarchical filters
        if class_filter:
            # class_filter now contains level_number, not ID
            questions = questions.filter(topic__class_level__level_number=class_filter)
        if subject_filter:
            # Filter by subject - need to check the correct relationship path
            try:
                # Try the direct relationship first
                questions = questions.filter(topic__class_level__subject_id=subject_filter)
            except:
                # If that fails, try alternative relationship paths
                try:
                    questions = questions.filter(topic__class_level__subject=subject_filter)
                except:
                    # Last resort: filter through topics that belong to the subject
                    valid_topics = Topic.objects.filter(class_level__subject_id=subject_filter).values_list('id', flat=True)
                    questions = questions.filter(topic_id__in=valid_topics)
        if topic_filter:
            questions = questions.filter(topic_id=topic_filter)
        if type_filter:
            questions = questions.filter(question_type=type_filter)
        if search_query:
            questions = questions.filter(question_text__icontains=search_query)

        # Order by class level, then subject, then topic, then question type
        questions = questions.order_by(
            'topic__class_level__level_number',
            'topic__class_level__subject__name',
            'topic__title',
            'question_type',
            '-created_at'
        )

        # Optimized pagination with larger page sizes for better performance
        page_size = min(int(self.request.GET.get('page_size', 100)), 500)  # Default 100, max 500
        paginator = Paginator(questions, page_size)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['questions'] = page_obj
        context['page_size'] = page_size
        context['total_questions'] = paginator.count

        # Get hierarchical filter options - distinct grade levels only
        # Group by level_number to avoid duplicates across subjects
        class_levels_raw = ClassLevel.objects.filter(is_active=True).values(
            'level_number'
        ).annotate(
            name=models.Min('name')  # Take the first name for this level
        ).order_by('level_number')

        # Convert to a list of objects that the template can use
        context['class_levels'] = [
            {
                'id': level['level_number'],  # Use level_number as ID for filtering
                'name': f"Grade {level['level_number']}",  # Standardize the name
                'level_number': level['level_number']
            }
            for level in class_levels_raw
        ]

        # Get subjects based on selected class level
        if class_filter:
            context['subjects'] = Subject.objects.filter(
                classlevels__level_number=class_filter,
                is_active=True
            ).distinct().order_by('name')
        else:
            context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')

        # Get topics based on selected class and subject (hierarchical filtering)
        topics_query = Topic.objects.filter(is_active=True).select_related('class_level__subject')

        # Apply hierarchical filters for topics
        if class_filter and subject_filter:
            # Both class and subject selected - filter by both
            try:
                topics_query = topics_query.filter(
                    class_level__level_number=class_filter,
                    class_level__subject_id=subject_filter
                )
            except:
                # Alternative approach if relationship is different
                try:
                    topics_query = topics_query.filter(
                        class_level__level_number=class_filter,
                        class_level__subject=subject_filter
                    )
                except:
                    # Last resort: get valid class levels first
                    valid_class_levels = ClassLevel.objects.filter(
                        level_number=class_filter,
                        subject_id=subject_filter
                    ).values_list('id', flat=True)
                    topics_query = topics_query.filter(class_level_id__in=valid_class_levels)
        elif class_filter:
            # Only class selected - show topics for that class level
            topics_query = topics_query.filter(class_level__level_number=class_filter)
        elif subject_filter:
            # Only subject selected - show topics for that subject across all classes
            try:
                topics_query = topics_query.filter(class_level__subject_id=subject_filter)
            except:
                # Alternative approach
                try:
                    topics_query = topics_query.filter(class_level__subject=subject_filter)
                except:
                    # Last resort
                    valid_class_levels = ClassLevel.objects.filter(subject_id=subject_filter).values_list('id', flat=True)
                    topics_query = topics_query.filter(class_level_id__in=valid_class_levels)

        context['topics'] = topics_query.order_by('class_level__level_number', 'title')

        # Current filter values
        context['current_filters'] = {
            'class_level': class_filter,
            'subject': subject_filter,
            'topic': topic_filter,
            'type': type_filter,
            'search': search_query,
        }

        # Statistics
        context['stats'] = {
            'total_questions': questions.count(),
            'active_questions': questions.filter(is_active=True).count(),
            'multiple_choice': questions.filter(question_type='multiple_choice').count(),
            'fill_blank': questions.filter(question_type='fill_blank').count(),
        }

        return context


class EditLevelView(AdminRequiredMixin, UpdateView):
    """View for editing class levels"""
    model = ClassLevel
    form_class = ClassLevelForm
    template_name = 'admin_panel/edit_level.html'
    success_url = reverse_lazy('admin_panel:levels')
    pk_url_kwarg = 'level_id'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='UPDATE_LEVEL',
            description=f'Updated level: {self.object.name}',
            model_name='ClassLevel',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Level "{self.object.name}" updated successfully!')
        return response


class DeleteLevelView(AdminRequiredMixin, DeleteView):
    """View for deleting class levels"""
    model = ClassLevel
    success_url = reverse_lazy('admin_panel:levels')
    pk_url_kwarg = 'level_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        level_name = self.object.name

        # Log activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DELETE_LEVEL',
            description=f'Deleted level: {level_name}',
            model_name='ClassLevel',
            object_id=str(self.object.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'Level "{level_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CreateTopicView(AdminRequiredMixin, CreateView):
    """View for creating new topics"""
    model = Topic
    form_class = TopicForm
    template_name = 'admin_panel/create_topic.html'
    success_url = reverse_lazy('admin_panel:topics')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='CREATE_TOPIC',
            description=f'Created topic: {self.object.title}',
            model_name='Topic',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Topic "{self.object.title}" created successfully!')
        return response


class EditTopicView(AdminRequiredMixin, UpdateView):
    """View for editing topics"""
    model = Topic
    form_class = TopicForm
    template_name = 'admin_panel/edit_topic.html'
    success_url = reverse_lazy('admin_panel:topics')
    pk_url_kwarg = 'topic_id'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='UPDATE_TOPIC',
            description=f'Updated topic: {self.object.title}',
            model_name='Topic',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'Topic "{self.object.title}" updated successfully!')
        return response


class DeleteTopicView(AdminRequiredMixin, DeleteView):
    """View for deleting topics"""
    model = Topic
    success_url = reverse_lazy('admin_panel:topics')
    pk_url_kwarg = 'topic_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        topic_title = self.object.title

        # Log activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DELETE_TOPIC',
            description=f'Deleted topic: {topic_title}',
            model_name='Topic',
            object_id=str(self.object.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'Topic "{topic_title}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CreateQuestionView(AdminRequiredMixin, CreateView):
    """View for creating new questions"""
    model = Question
    form_class = QuestionForm
    template_name = 'admin_panel/create_question.html'
    success_url = reverse_lazy('admin_panel:questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AnswerChoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = AnswerChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.created_by = self.request.user
            self.object.save()
            formset.instance = self.object
            formset.save()

            # Log activity
            AdminActivity.objects.create(
                admin_user=self.request.user,
                action='CREATE_QUESTION',
                description=f'Created question: {self.object.question_text[:50]}...',
                model_name='Question',
                object_id=str(self.object.id),
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(self.request, 'Question created successfully!')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditQuestionView(AdminRequiredMixin, UpdateView):
    """View for editing questions"""
    model = Question
    form_class = QuestionForm
    template_name = 'admin_panel/edit_question.html'
    success_url = reverse_lazy('admin_panel:questions')
    pk_url_kwarg = 'question_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = AnswerChoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = AnswerChoiceFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            # Log activity
            AdminActivity.objects.create(
                admin_user=self.request.user,
                action='UPDATE_QUESTION',
                description=f'Updated question: {self.object.question_text[:50]}...',
                model_name='Question',
                object_id=str(self.object.id),
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(self.request, 'Question updated successfully!')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DeleteQuestionView(AdminRequiredMixin, DeleteView):
    """View for deleting questions"""
    model = Question
    success_url = reverse_lazy('admin_panel:questions')
    pk_url_kwarg = 'question_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        question_text = self.object.question_text[:50]

        # Log activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DELETE_QUESTION',
            description=f'Deleted question: {question_text}...',
            model_name='Question',
            object_id=str(self.object.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, 'Question deleted successfully!')
        return super().delete(request, *args, **kwargs)


class CSVImportView(AdminRequiredMixin, TemplateView):
    """Clean CSV import for questions only"""
    template_name = 'admin_panel/csv_import.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Import form and recent imports
        context['form'] = CSVImportForm()
        context['recent_imports'] = CSVImportLog.objects.filter(
            imported_by=self.request.user,
            import_type='questions'
        ).order_by('-started_at')[:10]

        # Import instructions
        from core.utils.csv_samples import get_import_instructions
        context['import_instructions'] = get_import_instructions()

        # Content statistics
        context['content_stats'] = {
            'subjects_count': Subject.objects.count(),
            'levels_count': ClassLevel.objects.count(),
            'topics_count': Topic.objects.count(),
            'questions_count': Question.objects.count(),
        }

        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', 'import')

        if action == 'preview':
            return self.handle_preview(request)
        elif action == 'import':
            return self.handle_import(request)

        return self.get(request, *args, **kwargs)

    def handle_preview(self, request):
        """Handle CSV preview request"""
        # For preview, we only need the CSV file, not the class levels
        if 'csv_file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'No CSV file provided'
            })

        csv_file = request.FILES['csv_file']

        # Basic file validation
        if not csv_file.name.lower().endswith('.csv'):
            return JsonResponse({
                'success': False,
                'error': 'Please upload a CSV file'
            })

        if csv_file.size > 5 * 1024 * 1024:  # 5MB limit
            return JsonResponse({
                'success': False,
                'error': 'File size cannot exceed 5MB'
            })

        try:
            # Try multiple encodings to handle different file formats
            file_content = None
            encoding_used = None

            # List of encodings to try in order
            encodings_to_try = [
                'utf-8',           # Standard UTF-8
                'utf-8-sig',       # UTF-8 with BOM (Excel often saves this way)
                'latin1',          # Windows-1252 / ISO-8859-1
                'cp1252',          # Windows-1252 (common in Windows Excel)
                'iso-8859-1',      # ISO Latin-1
                'ascii'            # Basic ASCII
            ]

            csv_bytes = csv_file.read()

            for encoding in encodings_to_try:
                try:
                    file_content = csv_bytes.decode(encoding)
                    encoding_used = encoding
                    break
                except UnicodeDecodeError:
                    continue

            if file_content is None:
                return JsonResponse({
                    'success': False,
                    'error': 'Unable to read file. The file may contain unsupported characters or be corrupted. Please save your CSV file as UTF-8 encoding or try removing special characters.'
                })

            # Parse and validate CSV
            from core.utils.csv_import import CSVImporter
            importer = CSVImporter('questions', file_content, request.user)

            # Get preview data
            preview_data = importer.get_preview_data()

            # Add encoding info to response for debugging
            preview_data['encoding_info'] = {
                'detected_encoding': encoding_used,
                'file_size_bytes': len(csv_bytes)
            }

            return JsonResponse({
                'success': True,
                'preview_data': preview_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Preview failed: {str(e)}'
            })

    def handle_import(self, request):
        """Handle actual CSV import"""
        # For import, we need to validate the form properly
        form = CSVImportForm(request.POST, request.FILES)

        # Make target_class_levels required for actual import
        form.fields['target_class_levels'].required = True

        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            target_class_levels = form.cleaned_data['target_class_levels']
            import_mode = request.POST.get('import_mode', 'strict')  # Get import mode

            try:
                # Try multiple encodings to handle different file formats
                file_content = None
                encoding_used = None

                # List of encodings to try in order
                encodings_to_try = [
                    'utf-8',           # Standard UTF-8
                    'utf-8-sig',       # UTF-8 with BOM (Excel often saves this way)
                    'latin1',          # Windows-1252 / ISO-8859-1
                    'cp1252',          # Windows-1252 (common in Windows Excel)
                    'iso-8859-1',      # ISO Latin-1
                    'ascii'            # Basic ASCII
                ]

                csv_bytes = csv_file.read()

                for encoding in encodings_to_try:
                    try:
                        file_content = csv_bytes.decode(encoding)
                        encoding_used = encoding
                        break
                    except UnicodeDecodeError:
                        continue

                if file_content is None:
                    messages.error(request, 'Unable to read file. The file may contain unsupported characters or be corrupted. Please save your CSV file as UTF-8 encoding or try removing special characters.')
                    return redirect('admin_panel:csv_import')

                # Import questions with specified mode and progress tracking
                from core.utils.csv_import import CSVImporter
                import time

                start_time = time.time()
                print(f"🚀 Starting CSV import with mode: {import_mode}")

                importer = CSVImporter('questions', file_content, request.user, import_mode)
                result = importer.import_data()

                end_time = time.time()
                import_duration = end_time - start_time
                print(f"⏱️ Import completed in {import_duration:.2f} seconds")

                # Add performance info to result
                result['import_duration'] = round(import_duration, 2)
                result['questions_per_second'] = round(result.get('successful_rows', 0) / import_duration, 2) if import_duration > 0 else 0

                if result['success']:
                    # Log successful import activity
                    AdminActivity.objects.create(
                        admin_user=request.user,
                        action='CSV_IMPORT',
                        description=f'Imported questions (Mode: {import_mode}): {result["successful_rows"]} successful, {result.get("skipped_rows", result["failed_rows"])} skipped/failed',
                        model_name='CSVImport',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )

                    # Handle different import modes and results
                    if import_mode == 'partial':
                        if result.get("skipped_rows", 0) > 0:
                            messages.success(
                                request,
                                f'✅ Partial import completed! {result["successful_rows"]} questions imported successfully. '
                                f'{result["skipped_rows"]} rows with errors were skipped. '
                                f'⚡ Performance: {result["import_duration"]}s ({result["questions_per_second"]} questions/sec)'
                            )

                            # Show details about skipped rows
                            if result.get('skipped_details'):
                                skipped_summary = []
                                for skip in result['skipped_details'][:3]:  # Show first 3 errors
                                    skipped_summary.append(f"Row {skip['row_number']}: {skip['error']}")
                                if len(result['skipped_details']) > 3:
                                    skipped_summary.append(f"... and {len(result['skipped_details']) - 3} more errors")

                                messages.info(request, f"📋 Skipped rows details:\n• " + "\n• ".join(skipped_summary))
                        else:
                            messages.success(
                                request,
                                f'✅ Import completed successfully! {result["successful_rows"]} questions imported. '
                                f'⚡ Performance: {result["import_duration"]}s ({result["questions_per_second"]} questions/sec)'
                            )
                    else:
                        # Strict mode
                        if result["failed_rows"] > 0:
                            messages.warning(
                                request,
                                f'⚠️ Import partially completed! {result["successful_rows"]} questions imported. '
                                f'{result["failed_rows"]} failed. Check the import log for details.'
                            )
                        else:
                            messages.success(
                                request,
                                f'✅ Import completed successfully! {result["successful_rows"]} questions imported. '
                                f'⚡ Performance: {result["import_duration"]}s ({result["questions_per_second"]} questions/sec)'
                            )
                else:
                    messages.error(request, f'Import failed: {result["error"]}')

            except Exception as e:
                # Log failed import activity
                AdminActivity.objects.create(
                    admin_user=request.user,
                    action='CSV_IMPORT_FAILED',
                    description=f'Failed to import questions: {str(e)}',
                    model_name='CSVImport',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                messages.error(request, f'Import failed: {str(e)}')

            return redirect('admin_panel:csv_import')

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class DownloadTemplateView(AdminRequiredMixin, View):
    """View for downloading questions CSV template"""

    def get(self, request, *args, **kwargs):
        include_samples = request.GET.get('samples', 'true').lower() == 'true'

        from core.utils.csv_samples import create_csv_content

        # Get CSV content with or without samples
        if include_samples:
            csv_content = create_csv_content()
            filename = "questions_template_with_samples.csv"
        else:
            from core.utils.csv_import import get_csv_template
            headers = get_csv_template('questions')
            csv_content = ','.join(headers) + '\n'
            filename = "questions_template.csv"

        if not csv_content:
            messages.error(request, 'Template not available')
            return redirect('admin_panel:csv_import')

        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Log template download activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DOWNLOAD_TEMPLATE',
            description=f'Downloaded questions CSV template (samples: {include_samples})',
            model_name='CSVTemplate',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return response


class ExportQuestionsView(AdminRequiredMixin, View):
    """Export all questions to CSV"""

    def get(self, request, *args, **kwargs):
        import csv
        from io import StringIO

        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            'subject_name', 'class_level_name', 'topic_title', 'question_text', 'question_type',
            'correct_answer', 'explanation', 'difficulty', 'points', 'time_limit',
            'choice_a', 'choice_b', 'choice_c', 'choice_d'
        ]
        writer.writerow(header)

        # Get all questions with related data
        questions = Question.objects.select_related(
            'topic__class_level__subject'
        ).prefetch_related('answer_choices').filter(is_active=True)

        for question in questions:
            # Get choices for multiple choice questions
            choices = ['', '', '', '']
            if question.question_type == 'multiple_choice':
                answer_choices = question.answer_choices.all().order_by('order')
                for i, choice in enumerate(answer_choices[:4]):
                    choices[i] = choice.choice_text

            row = [
                question.topic.class_level.subject.name,
                question.topic.class_level.name,
                question.topic.title,
                question.question_text,
                question.question_type,
                question.correct_answer,
                question.explanation,
                question.difficulty,
                question.points,
                question.time_limit,
                choices[0], choices[1], choices[2], choices[3]
            ]
            writer.writerow(row)

        # Create response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questions_export.csv"'

        # Log export activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='EXPORT_QUESTIONS',
            description=f'Exported {questions.count()} questions to CSV',
            model_name='Question',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return response


class ExportUsersView(AdminRequiredMixin, View):
    """Export all users to CSV"""

    def get(self, request, *args, **kwargs):
        import csv
        from io import StringIO
        from django.db import models

        # Create CSV content
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        header = [
            'email', 'first_name', 'last_name', 'current_grade', 'date_joined',
            'is_active', 'total_quizzes', 'average_score', 'subjects_completed'
        ]
        writer.writerow(header)

        # Get all users with progress data
        users = User.objects.filter(is_staff=False).prefetch_related('quizzes')

        for user in users:
            # Calculate user statistics
            quizzes = user.quizzes.all()
            total_quizzes = quizzes.count()
            average_score = quizzes.aggregate(avg_score=models.Avg('percentage'))['avg_score'] or 0

            # Get completed subjects count
            completed_subjects = user.progress.filter(is_completed=True).values('topic__class_level__subject').distinct().count()

            row = [
                user.email,
                user.first_name,
                user.last_name,
                user.current_grade.name if user.current_grade else '',
                user.date_joined.strftime('%Y-%m-%d'),
                user.is_active,
                total_quizzes,
                round(average_score, 1),
                completed_subjects
            ]
            writer.writerow(row)

        # Create response
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'

        # Log export activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='EXPORT_USERS',
            description=f'Exported {users.count()} users to CSV',
            model_name='User',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return response


class CreateUserView(AdminRequiredMixin, CreateView):
    """View for creating new users"""
    model = User
    form_class = UserEditForm
    template_name = 'admin_panel/create_user.html'
    success_url = reverse_lazy('admin_panel:users')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'User "{self.object.full_name}" created successfully!')

        # Log admin activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='CREATE',
            description=f'Created user: {self.object.full_name}'
        )
        return response


class ManageUsersView(AdminRequiredMixin, TemplateView):
    """View for managing users"""
    template_name = 'admin_panel/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all users with related data
        users = User.objects.annotate(
            quizzes_count=Count('quizzes'),
            progress_count=Count('progress')
        ).order_by('-date_joined')

        # Apply filters
        search = self.request.GET.get('search')
        if search:
            users = users.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
        elif status_filter == 'staff':
            users = users.filter(is_staff=True)

        # Pagination
        paginator = Paginator(users, 20)
        page_number = self.request.GET.get('page')
        context['users'] = paginator.get_page(page_number)

        return context


class EditUserView(AdminRequiredMixin, UpdateView):
    """View for editing users"""
    model = User
    form_class = UserEditForm
    template_name = 'admin_panel/edit_user.html'
    success_url = reverse_lazy('admin_panel:users')
    pk_url_kwarg = 'user_id'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Log activity
        AdminActivity.objects.create(
            admin_user=self.request.user,
            action='UPDATE_USER',
            description=f'Updated user: {self.object.full_name}',
            model_name='User',
            object_id=str(self.object.id),
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(self.request, f'User "{self.object.full_name}" updated successfully!')
        return response


class DeleteUserView(AdminRequiredMixin, DeleteView):
    """View for deleting users"""
    model = User
    success_url = reverse_lazy('admin_panel:users')
    pk_url_kwarg = 'user_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_name = self.object.full_name

        # Prevent deleting superusers
        if self.object.is_superuser:
            messages.error(request, 'Cannot delete superuser accounts!')
            return redirect(self.success_url)

        # Log activity
        AdminActivity.objects.create(
            admin_user=request.user,
            action='DELETE_USER',
            description=f'Deleted user: {user_name}',
            model_name='User',
            object_id=str(self.object.id),
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        messages.success(request, f'User "{user_name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ReportsView(AdminRequiredMixin, TemplateView):
    """View for analytics and reports"""
    template_name = 'admin_panel/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Date range for reports
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_7_days = today - timedelta(days=7)

        # User analytics
        context['user_stats'] = {
            'total_users': User.objects.count(),
            'new_users_30_days': User.objects.filter(date_joined__gte=last_30_days).count(),
            'new_users_7_days': User.objects.filter(date_joined__gte=last_7_days).count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'staff_users': User.objects.filter(is_staff=True).count(),
        }

        # Quiz analytics
        context['quiz_stats'] = {
            'total_quizzes': Quiz.objects.count(),
            'completed_quizzes': Quiz.objects.filter(is_completed=True).count(),
            'quizzes_30_days': Quiz.objects.filter(started_at__gte=last_30_days).count(),
            'average_score': Quiz.objects.filter(is_completed=True).aggregate(
                avg=Avg('percentage')
            )['avg'] or 0,
        }

        # Content analytics
        context['content_stats'] = {
            'total_subjects': Subject.objects.count(),
            'total_levels': ClassLevel.objects.count(),
            'total_topics': Topic.objects.count(),
            'total_questions': Question.objects.count(),
            'active_questions': Question.objects.filter(is_active=True).count(),
        }

        # Recent activity
        context['recent_activities'] = AdminActivity.objects.select_related('admin_user')[:20]

        # Top performing topics
        context['top_topics'] = Topic.objects.annotate(
            quiz_count=Count('quizzes')
        ).order_by('-quiz_count')[:10]

        return context


class SiteSettingsView(AdminRequiredMixin, TemplateView):
    """View for managing site settings"""
    template_name = 'admin_panel/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.get_settings()
        context['form'] = SiteSettingsForm(instance=settings)
        context['settings'] = settings
        return context

    def post(self, request, *args, **kwargs):
        settings = SiteSettings.get_settings()
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)

        if form.is_valid():
            try:
                updated_settings = form.save(commit=False)
                updated_settings.updated_by = request.user
                updated_settings.save()

                # Log activity
                AdminActivity.objects.create(
                    admin_user=request.user,
                    action='UPDATE_SETTINGS',
                    description='Updated site settings',
                    model_name='SiteSettings',
                    object_id=str(settings.id),
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )

                # Provide specific success feedback
                updated_fields = []
                if 'site_logo' in request.FILES:
                    updated_fields.append('Site Logo')
                if 'site_favicon' in request.FILES:
                    updated_fields.append('Site Favicon')
                if 'hero_banner' in request.FILES:
                    updated_fields.append('Hero Banner')

                if updated_fields:
                    messages.success(request, f'Settings updated successfully! Updated: {", ".join(updated_fields)}')
                else:
                    messages.success(request, 'Settings updated successfully!')

                return redirect('admin_panel:settings')

            except Exception as e:
                messages.error(request, f'Error saving settings: {str(e)}')

        else:
            # Provide detailed error feedback
            error_messages = []
            for field, errors in form.errors.items():
                field_name = form.fields[field].label or field.replace('_', ' ').title()
                for error in errors:
                    error_messages.append(f"{field_name}: {error}")

            if error_messages:
                messages.error(request, f'Please fix the following errors: {"; ".join(error_messages)}')
            else:
                messages.error(request, 'Please check the form for errors.')

        # Return form with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


# API Views for AJAX functionality
class SubjectsAPIView(AdminRequiredMixin, View):
    """API view for subjects data"""

    def get(self, request, *args, **kwargs):
        subjects = Subject.objects.filter(is_active=True).values('id', 'name', 'color', 'icon')
        return JsonResponse({'subjects': list(subjects)})


class LevelsAPIView(AdminRequiredMixin, View):
    """API view for levels data"""

    def get(self, request, *args, **kwargs):
        subject_id = request.GET.get('subject_id')
        levels = ClassLevel.objects.filter(is_active=True)

        if subject_id:
            levels = levels.filter(subject_id=subject_id)

        levels_data = levels.values('id', 'name', 'level_number', 'subject__name')
        return JsonResponse({'levels': list(levels_data)})


class TopicsAPIView(AdminRequiredMixin, View):
    """API view for topics data"""

    def get(self, request, *args, **kwargs):
        level_id = request.GET.get('level_id')
        topics = Topic.objects.filter(is_active=True)

        if level_id:
            topics = topics.filter(class_level_id=level_id)

        topics_data = topics.values('id', 'title', 'class_level__name', 'class_level__subject__name')
        return JsonResponse({'topics': list(topics_data)})


class QuestionsAPIView(AdminRequiredMixin, View):
    """API view for questions data"""

    def get(self, request, *args, **kwargs):
        topic_id = request.GET.get('topic_id')
        questions = Question.objects.filter(is_active=True)

        if topic_id:
            questions = questions.filter(topic_id=topic_id)

        questions_data = questions.values(
            'id', 'question_text', 'question_type', 'difficulty', 'points',
            'topic__title', 'topic__class_level__name'
        )
        return JsonResponse({'questions': list(questions_data)})


class ManageStudyNotesView(AdminRequiredMixin, TemplateView):
    """View for managing study notes with hierarchical selection"""
    template_name = 'admin_panel/manage_study_notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # NEW FLOW: Grade Level → Subject → Topic
        # Get selected filters from GET parameters
        level_id = self.request.GET.get('level_id')
        subject_id = self.request.GET.get('subject_id')
        topic_id = self.request.GET.get('topic_id')

        context['selected_level_id'] = level_id
        context['selected_subject_id'] = subject_id
        context['selected_topic_id'] = topic_id

        # Get all grade levels for initial dropdown (1-12)
        context['levels'] = ClassLevel.objects.filter(
            is_active=True
        ).values('level_number').distinct().order_by('level_number')

        # Get subjects if grade level is selected
        if level_id:
            try:
                # level_id is now the level_number (e.g., 5 for Grade 5)
                level_number = int(level_id)
                context['subjects'] = Subject.objects.filter(
                    classlevels__level_number=level_number,
                    is_active=True
                ).distinct().order_by('name')
            except (ValueError, TypeError):
                context['subjects'] = Subject.objects.none()

        # Get topics if grade level and subject are selected
        if level_id and subject_id:
            try:
                # Find the ClassLevel that matches both level_number and subject_id
                level_number = int(level_id)
                level = ClassLevel.objects.get(
                    level_number=level_number,
                    subject_id=subject_id,
                    is_active=True
                )
                context['topics'] = Topic.objects.filter(
                    class_level=level,
                    is_active=True
                ).order_by('title')
            except (ClassLevel.DoesNotExist, ValueError, TypeError):
                context['topics'] = Topic.objects.none()

        # Get study notes if topic is selected
        if topic_id:
            study_notes_list = StudyNote.objects.filter(
                topic_id=topic_id
            ).order_by('order', 'created_at')

            # Pagination
            paginator = Paginator(study_notes_list, 15)  # 15 notes per page
            page = self.request.GET.get('page', 1)

            try:
                study_notes = paginator.page(page)
            except PageNotAnInteger:
                study_notes = paginator.page(1)
            except EmptyPage:
                study_notes = paginator.page(paginator.num_pages)

            context['study_notes'] = study_notes
            context['is_paginated'] = paginator.num_pages > 1

        return context


class CreateStudyNoteView(AdminRequiredMixin, View):
    """View for creating study notes"""

    def get(self, request):
        # NEW FLOW: Grade Level → Subject → Topic
        level_id = request.GET.get('level_id')
        subject_id = request.GET.get('subject_id')
        topic_id = request.GET.get('topic_id')

        context = {
            'selected_level_id': level_id,
            'selected_subject_id': subject_id,
            'selected_topic_id': topic_id,
        }

        # Get all grade levels for initial dropdown
        context['levels'] = ClassLevel.objects.filter(
            is_active=True
        ).values('level_number').distinct().order_by('level_number')

        # Get subjects if grade level is selected
        if level_id:
            try:
                # level_id is now the level_number (e.g., 5 for Grade 5)
                level_number = int(level_id)
                context['subjects'] = Subject.objects.filter(
                    classlevels__level_number=level_number,
                    is_active=True
                ).distinct().order_by('name')
            except (ValueError, TypeError):
                context['subjects'] = Subject.objects.none()

        # Get topics if grade level and subject are selected
        if level_id and subject_id:
            try:
                # Find the ClassLevel that matches both level_number and subject_id
                level_number = int(level_id)
                level = ClassLevel.objects.get(
                    level_number=level_number,
                    subject_id=subject_id,
                    is_active=True
                )
                context['topics'] = Topic.objects.filter(
                    class_level=level,
                    is_active=True
                ).order_by('title')
            except (ClassLevel.DoesNotExist, ValueError, TypeError):
                context['topics'] = Topic.objects.none()

        return render(request, 'admin_panel/create_study_note.html', context)

    def post(self, request):
        subject_id = request.POST.get('subject_id')
        level_id = request.POST.get('level_id')
        topic_id = request.POST.get('topic_id')
        topic_title = request.POST.get('topic_title', '').strip()
        note_title = request.POST.get('note_title', '').strip()
        content = request.POST.get('content', '').strip()

        if not all([subject_id, level_id, note_title, content]):
            messages.error(request, 'Please fill in all required fields.')
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(f"{request.path}?subject_id={subject_id}&level_id={level_id}&topic_id={topic_id}")

        try:
            # Get the class level that matches both level_number and subject_id
            level_number = int(level_id)  # level_id is now level_number
            level = ClassLevel.objects.get(level_number=level_number, subject_id=subject_id, is_active=True)

            # Create topic if it doesn't exist
            if topic_id:
                topic = Topic.objects.get(id=topic_id, class_level=level, is_active=True)
            elif topic_title:
                topic, created = Topic.objects.get_or_create(
                    title=topic_title,
                    class_level=level,
                    defaults={
                        'description': f'Study materials for {topic_title}',
                        'is_active': True
                    }
                )
                if created:
                    messages.success(request, f'Created new topic: {topic_title}')
            else:
                messages.error(request, 'Please select an existing topic or provide a title for a new topic.')
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect(f"{request.path}?subject_id={subject_id}&level_id={level_id}")

            # Check for potential duplicate (same title and topic within last 5 seconds)
            from django.utils import timezone
            from datetime import timedelta

            recent_cutoff = timezone.now() - timedelta(seconds=5)
            existing_note = StudyNote.objects.filter(
                topic=topic,
                title=note_title,
                created_by=request.user,
                created_at__gte=recent_cutoff
            ).first()

            if existing_note:
                messages.warning(request, f'Study note "{note_title}" was already created recently.')
                from django.http import HttpResponseRedirect
                from django.urls import reverse
                url = reverse('admin_panel:manage_study_notes')
                return HttpResponseRedirect(f'{url}?subject_id={subject_id}&level_id={level_id}&topic_id={topic.id}')

            # Create study note
            StudyNote.objects.create(
                topic=topic,
                title=note_title,
                content=content,
                created_by=request.user
            )

            messages.success(request, f'Study note "{note_title}" created successfully!')
            # Redirect with query parameters
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            url = reverse('admin_panel:manage_study_notes')
            return HttpResponseRedirect(f'{url}?subject_id={subject_id}&level_id={level_id}&topic_id={topic.id}')

        except (ClassLevel.DoesNotExist, Topic.DoesNotExist, ValueError, TypeError):
            messages.error(request, 'Invalid selection. Please try again.')
            return redirect('admin_panel:manage_study_notes')


class ImportLogsView(AdminRequiredMixin, ListView):
    """View for displaying import logs"""
    model = CSVImportLog
    template_name = 'admin_panel/import_logs.html'
    context_object_name = 'logs'
    paginate_by = 20
    ordering = ['-started_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add statistics
        context['stats'] = {
            'total_imports': CSVImportLog.objects.count(),
            'successful_imports': CSVImportLog.objects.filter(status='completed').count(),
            'failed_imports': CSVImportLog.objects.filter(status='failed').count(),
            'partial_imports': CSVImportLog.objects.filter(status='partial').count(),
        }

        # Filter options
        status_filter = self.request.GET.get('status')
        import_type_filter = self.request.GET.get('import_type')

        context['current_status_filter'] = status_filter
        context['current_import_type_filter'] = import_type_filter

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply filters
        status_filter = self.request.GET.get('status')
        import_type_filter = self.request.GET.get('import_type')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if import_type_filter:
            queryset = queryset.filter(import_type=import_type_filter)

        return queryset


class ImportLogDetailView(AdminRequiredMixin, DetailView):
    """View for displaying detailed import log information"""
    model = CSVImportLog
    template_name = 'admin_panel/import_log_detail.html'
    context_object_name = 'log'
    pk_url_kwarg = 'log_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Parse error log into individual errors
        if self.object.error_log:
            context['errors'] = self.object.error_log.strip().split('\n')
        else:
            context['errors'] = []

        return context


class DeleteImportLogView(AdminRequiredMixin, View):
    """View for deleting import logs"""

    def post(self, request, log_id):
        try:
            log = CSVImportLog.objects.get(id=log_id)
            log_name = f"{log.import_type} - {log.file_name}"
            log.delete()

            # Log admin activity
            AdminActivity.objects.create(
                admin_user=request.user,
                action='DELETE_IMPORT_LOG',
                description=f'Deleted import log: {log_name}',
                model_name='CSVImportLog',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(request, f'Import log "{log_name}" deleted successfully.')

        except CSVImportLog.DoesNotExist:
            messages.error(request, 'Import log not found.')
        except Exception as e:
            messages.error(request, f'Error deleting import log: {str(e)}')

        return redirect('admin_panel:import_logs')


class StudyNoteDetailView(AdminRequiredMixin, View):
    """AJAX view for getting study note details"""

    def get(self, request, note_id):
        try:
            note = StudyNote.objects.select_related(
                'topic__class_level__subject',
                'created_by'
            ).get(id=note_id)

            data = {
                'success': True,
                'title': note.title,
                'content': note.content,
                'created_by': note.created_by.get_full_name() if note.created_by else 'System',
                'created_at': note.created_at.strftime('%B %d, %Y at %I:%M %p'),
                'updated_at': note.updated_at.strftime('%B %d, %Y at %I:%M %p'),
                'topic': note.topic.title,
                'subject': note.topic.class_level.subject.name,
                'grade': f"Grade {note.topic.class_level.level_number}"
            }
            return JsonResponse(data)
        except StudyNote.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Study note not found'
            }, status=404)


class EditStudyNoteView(AdminRequiredMixin, View):
    """View for editing study notes"""

    def get(self, request, note_id):
        try:
            note = StudyNote.objects.select_related(
                'topic__class_level__subject'
            ).get(id=note_id)

            # Get all subjects for the form
            subjects = Subject.objects.filter(is_active=True).order_by('name')

            # Get levels for the selected subject
            levels = ClassLevel.objects.filter(
                subject=note.topic.class_level.subject,
                is_active=True
            ).order_by('level_number')

            # Get topics for the selected level
            topics = Topic.objects.filter(
                class_level=note.topic.class_level,
                is_active=True
            ).order_by('title')

            context = {
                'note': note,
                'subjects': subjects,
                'levels': levels,
                'topics': topics,
                'selected_subject_id': str(note.topic.class_level.subject.id),
                'selected_level_id': str(note.topic.class_level.id),
                'selected_topic_id': str(note.topic.id),
            }

            return render(request, 'admin_panel/edit_study_note.html', context)

        except StudyNote.DoesNotExist:
            messages.error(request, 'Study note not found.')
            return redirect('admin_panel:manage_study_notes')

    def post(self, request, note_id):
        try:
            note = StudyNote.objects.get(id=note_id)

            # Get form data
            title = request.POST.get('note_title', '').strip()
            content = request.POST.get('content', '').strip()
            topic_id = request.POST.get('topic_id')

            # Validation
            if not title or not content:
                messages.error(request, 'Title and content are required.')
                return redirect('admin_panel:edit_study_note', note_id=note_id)

            # Handle topic selection or creation
            if topic_id:
                try:
                    topic = Topic.objects.get(id=topic_id)
                except Topic.DoesNotExist:
                    messages.error(request, 'Selected topic not found.')
                    return redirect('admin_panel:edit_study_note', note_id=note_id)
            else:
                # Create new topic if specified
                topic_title = request.POST.get('topic_title', '').strip()
                subject_id = request.POST.get('subject_id')
                level_id = request.POST.get('level_id')

                if not topic_title or not subject_id or not level_id:
                    messages.error(request, 'Please select an existing topic or provide details for a new topic.')
                    return redirect('admin_panel:edit_study_note', note_id=note_id)

                try:
                    class_level = ClassLevel.objects.get(id=level_id, subject_id=subject_id)
                    topic, created = Topic.objects.get_or_create(
                        title=topic_title,
                        class_level=class_level,
                        defaults={
                            'description': f'Auto-created topic for {topic_title}',
                            'created_by': request.user
                        }
                    )
                    if created:
                        messages.success(request, f'New topic "{topic_title}" created successfully.')
                except ClassLevel.DoesNotExist:
                    messages.error(request, 'Invalid subject and grade level combination.')
                    return redirect('admin_panel:edit_study_note', note_id=note_id)

            # Update the study note
            note.title = title
            note.content = content
            note.topic = topic
            note.save()

            # Log activity
            AdminActivity.objects.create(
                admin_user=request.user,
                action='UPDATE_STUDY_NOTE',
                description=f'Updated study note: {title}',
                model_name='StudyNote',
                object_id=str(note.id),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            messages.success(request, f'Study note "{title}" updated successfully!')
            return redirect('admin_panel:manage_study_notes')

        except StudyNote.DoesNotExist:
            messages.error(request, 'Study note not found.')
            return redirect('admin_panel:manage_study_notes')
        except Exception as e:
            messages.error(request, f'Error updating study note: {str(e)}')
            return redirect('admin_panel:edit_study_note', note_id=note_id)


class ReorderStudyNotesView(AdminRequiredMixin, View):
    """AJAX view for reordering study notes"""

    def post(self, request):
        try:
            import json
            data = json.loads(request.body)
            note_orders = data.get('note_orders', [])

            if not note_orders:
                return JsonResponse({'success': False, 'error': 'No note orders provided'})

            # Update note orders in a transaction
            from django.db import transaction
            with transaction.atomic():
                for item in note_orders:
                    note_id = item.get('id')
                    new_order = item.get('order')

                    if note_id and new_order is not None:
                        try:
                            note = StudyNote.objects.get(id=note_id)
                            note.order = new_order
                            note.save(update_fields=['order'])
                        except StudyNote.DoesNotExist:
                            continue

            return JsonResponse({
                'success': True,
                'message': 'Study notes reordered successfully'
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class DeleteStudyNoteView(AdminRequiredMixin, View):
    """View for deleting study notes"""

    def post(self, request, note_id):
        try:
            note = StudyNote.objects.get(id=note_id)
            note_title = note.title
            topic_id = note.topic.id
            subject_id = note.topic.class_level.subject.id
            level_id = note.topic.class_level.level_number

            # Log activity
            AdminActivity.objects.create(
                admin_user=request.user,
                action='DELETE_STUDY_NOTE',
                description=f'Deleted study note: {note_title}',
                model_name='StudyNote',
                object_id=str(note.id),
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Delete the note
            note.delete()

            messages.success(request, f'Study note "{note_title}" deleted successfully!')

            # Redirect back to manage study notes with the same filters
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            url = reverse('admin_panel:manage_study_notes')
            return HttpResponseRedirect(f'{url}?subject_id={subject_id}&level_id={level_id}&topic_id={topic_id}')

        except StudyNote.DoesNotExist:
            messages.error(request, 'Study note not found.')
            return redirect('admin_panel:manage_study_notes')
        except Exception as e:
            messages.error(request, f'Error deleting study note: {str(e)}')
            return redirect('admin_panel:manage_study_notes')


class ReadStudyNotesView(AdminRequiredMixin, TemplateView):
    """View for reading study notes with single-note pagination"""
    template_name = 'admin_panel/read_study_notes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic_id = self.kwargs.get('topic_id')
        note_index = int(self.request.GET.get('note', 1)) - 1  # Convert to 0-based index

        try:
            topic = Topic.objects.select_related(
                'class_level__subject'
            ).get(id=topic_id, is_active=True)

            # Get all study notes for this topic
            study_notes = StudyNote.objects.filter(
                topic=topic
            ).order_by('created_at')  # Order by creation date for consistent reading order

            if not study_notes.exists():
                context['error'] = 'No study notes found for this topic.'
                return context

            # Ensure note_index is within bounds
            if note_index < 0:
                note_index = 0
            elif note_index >= study_notes.count():
                note_index = study_notes.count() - 1

            current_note = study_notes[note_index]

            context.update({
                'topic': topic,
                'current_note': current_note,
                'current_index': note_index + 1,  # Convert back to 1-based for display
                'total_notes': study_notes.count(),
                'has_previous': note_index > 0,
                'has_next': note_index < study_notes.count() - 1,
                'previous_index': note_index if note_index <= 0 else note_index,
                'next_index': note_index + 2 if note_index < study_notes.count() - 1 else note_index + 1,
            })

        except Topic.DoesNotExist:
            context['error'] = 'Topic not found.'

        return context


class DuplicateQuestionsView(AdminRequiredMixin, TemplateView):
    """View for managing duplicate questions"""
    template_name = 'admin_panel/duplicate_questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all subjects and class levels for filtering
        context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')
        context['class_levels'] = ClassLevel.objects.filter(is_active=True).order_by('level_number')

        # Get statistics
        context['total_questions'] = Question.objects.count()
        context['active_questions'] = Question.objects.filter(is_active=True).count()

        return context


class DetectDuplicatesAPIView(AdminRequiredMixin, View):
    """Optimized API view for detecting duplicate questions with real-time progress"""

    def __init__(self):
        super().__init__()
        self.progress_data = {}  # Store progress for each request

    def similarity(self, a, b):
        """Calculate similarity between two strings"""
        return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

    def clean_question_text(self, text):
        """Clean question text for comparison"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\?\!\.\,\;\:]', '', text)
        return text.strip().lower()

    def post(self, request):
        try:
            import json
            import time
            data = json.loads(request.body)

            # Get filter parameters
            class_level_filter = data.get('class_level')
            subject_filter = data.get('subject')
            similarity_threshold = float(data.get('similarity_threshold', 0.85))
            request_id = data.get('request_id', 'default')

            print(f"🔍 Starting optimized duplicate detection with threshold: {similarity_threshold}")

            # Build optimized query with select_related for better performance
            questions = Question.objects.select_related(
                'topic__class_level__subject'
            ).filter(is_active=True)

            if class_level_filter:
                questions = questions.filter(topic__class_level__level_number=class_level_filter)
            if subject_filter:
                questions = questions.filter(topic__class_level__subject_id=subject_filter)

            # Count total questions first
            total_count = questions.count()
            print(f"📊 Found {total_count} questions to analyze")

            if total_count < 2:
                return JsonResponse({
                    'success': True,
                    'duplicates': [],
                    'total_groups': 0,
                    'total_duplicates': 0,
                    'similarity_threshold': similarity_threshold,
                    'processing_time': 0,
                    'questions_analyzed': total_count
                })

            # Use optimized duplicate detector
            from .duplicate_detector import OptimizedDuplicateDetector

            def progress_callback(message, percentage):
                """Store progress for potential real-time updates"""
                self.progress_data[request_id] = {
                    'message': message,
                    'percentage': percentage,
                    'timestamp': time.time()
                }
                print(f"📈 Progress: {percentage:.1f}% - {message}")

            detector = OptimizedDuplicateDetector(
                similarity_threshold=similarity_threshold,
                chunk_size=min(1000, total_count // 10 + 100)  # Dynamic chunk size
            )

            start_time = time.time()
            duplicate_groups = detector.find_duplicates_optimized(
                questions,
                progress_callback=progress_callback
            )
            end_time = time.time()

            processing_time = end_time - start_time
            total_duplicates = sum(group['count'] for group in duplicate_groups)

            print(f"✅ Duplicate detection completed in {processing_time:.2f}s")
            print(f"📋 Found {len(duplicate_groups)} groups with {total_duplicates} total duplicates")

            return JsonResponse({
                'success': True,
                'duplicates': duplicate_groups,
                'total_groups': len(duplicate_groups),
                'total_duplicates': total_duplicates,
                'similarity_threshold': similarity_threshold,
                'processing_time': round(processing_time, 2),
                'questions_analyzed': total_count,
                'performance_stats': {
                    'questions_per_second': round(total_count / processing_time, 2) if processing_time > 0 else 0,
                    'optimization_used': 'hash_based_chunking'
                }
            })

        except Exception as e:
            print(f"❌ Error in duplicate detection: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


class DeleteDuplicatesAPIView(AdminRequiredMixin, View):
    """API view for deleting duplicate questions with enhanced safety features"""

    def clean_question_text(self, text):
        """Clean question text for comparison (same as DetectDuplicatesAPIView)"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\?\!\.\,\;\:]', '', text)
        return text.strip().lower()

    def post(self, request):
        from django.db import transaction
        try:
            import json
            data = json.loads(request.body)

            action = data.get('action')  # 'selected', 'all_duplicates', 'group'
            question_ids = data.get('question_ids', [])
            group_id = data.get('group_id')

            # Debug logging
            print(f"DEBUG: Received deletion request")
            print(f"DEBUG: Action: {action}")
            print(f"DEBUG: Question IDs: {question_ids}")
            print(f"DEBUG: Number of question IDs: {len(question_ids)}")

            deleted_count = 0
            preserved_count = 0
            errors = []

            # Safety check: Ensure we have valid question IDs
            if not question_ids:
                print("DEBUG: No question IDs provided")
                return JsonResponse({
                    'success': False,
                    'error': 'No questions selected for deletion.'
                }, status=400)

            if action == 'selected':
                # Optimized bulk deletion for selected questions
                print(f"🗑️ Starting optimized bulk deletion of {len(question_ids)} questions...")

                # Use bulk operations for much faster deletion
                with transaction.atomic():
                    # First, bulk delete answer choices
                    answer_choices_deleted = AnswerChoice.objects.filter(question_id__in=question_ids).delete()
                    print(f"✅ Deleted {answer_choices_deleted[0]} answer choices")

                    # Then, bulk delete questions
                    questions_deleted = Question.objects.filter(id__in=question_ids).delete()
                    deleted_count = questions_deleted[0]
                    print(f"✅ Deleted {deleted_count} questions")

                # Log the bulk deletion activity
                try:
                    AdminActivity.objects.create(
                        admin_user=request.user,
                        action='BULK_DELETE_DUPLICATE_QUESTIONS',
                        description=f'Bulk deleted {deleted_count} duplicate questions',
                        model_name='Question',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                except Exception as e:
                    errors.append(f'Error logging bulk deletion: {str(e)}')

                preserved_count = 0

            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Invalid action: {action}. Only "selected" action is supported.'
                }, status=400)

            # Prepare response
            response_data = {
                'success': True,
                'deleted_count': deleted_count,
                'preserved_count': preserved_count,
                'message': f'Successfully deleted {deleted_count} duplicate questions.'
            }

            # Include errors if any occurred during logging
            if errors:
                response_data['warnings'] = errors
                response_data['message'] += f' Note: {len(errors)} logging errors occurred.'

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data provided.'
            }, status=400)
        except Exception as e:
            # Log the error for debugging
            AdminActivity.objects.create(
                admin_user=request.user,
                action='DELETE_DUPLICATE_ERROR',
                description=f'Error during duplicate deletion: {str(e)}',
                model_name='Question',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            return JsonResponse({
                'success': False,
                'error': f'An error occurred while deleting questions: {str(e)}'
            }, status=500)