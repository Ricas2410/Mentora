import csv
import io
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, View, ListView, DetailView
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.urls import reverse_lazy

from subjects.models import Subject, ClassLevel, Topic
from content.models import Question, AnswerChoice, StudyNote, Quiz
from users.models import User
from progress.models import UserProgress
from .models import SiteSettings, AdminActivity
from core.models import CSVImportLog
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
    """View for managing subjects"""
    template_name = 'admin_panel/subjects.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all subjects with related data
        subjects = Subject.objects.annotate(
            levels_count=Count('classlevels'),
            topics_count=Count('classlevels__topics'),
            questions_count=Count('classlevels__topics__questions')
        ).order_by('name')

        # Pagination
        paginator = Paginator(subjects, 10)
        page_number = self.request.GET.get('page')
        context['subjects'] = paginator.get_page(page_number)

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

        # Get all topics with related data
        topics = Topic.objects.select_related('class_level__subject').annotate(
            questions_count=Count('questions')
        ).order_by('class_level__subject__name', 'class_level__level_number', 'order')

        # Pagination
        paginator = Paginator(topics, 10)
        page_number = self.request.GET.get('page')
        context['topics'] = paginator.get_page(page_number)

        return context


class ManageQuestionsView(AdminRequiredMixin, TemplateView):
    """View for managing questions"""
    template_name = 'admin_panel/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter parameters
        subject_filter = self.request.GET.get('subject')
        level_filter = self.request.GET.get('level')
        topic_filter = self.request.GET.get('topic')
        type_filter = self.request.GET.get('type')
        search_query = self.request.GET.get('search')

        # Start with all questions
        questions = Question.objects.select_related('topic__class_level__subject').annotate(
            choices_count=Count('answer_choices')
        )

        # Apply filters
        if subject_filter:
            questions = questions.filter(topic__class_level__subject_id=subject_filter)
        if level_filter:
            questions = questions.filter(topic__class_level_id=level_filter)
        if topic_filter:
            questions = questions.filter(topic_id=topic_filter)
        if type_filter:
            questions = questions.filter(question_type=type_filter)
        if search_query:
            questions = questions.filter(question_text__icontains=search_query)

        # Order by creation date (newest first)
        questions = questions.order_by('-created_at')

        # Pagination
        paginator = Paginator(questions, 20)
        page_number = self.request.GET.get('page')
        context['questions'] = paginator.get_page(page_number)

        # Get filter options
        context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')
        context['levels'] = ClassLevel.objects.filter(is_active=True).select_related('subject').order_by('subject__name', 'level_number')
        context['topics'] = Topic.objects.filter(is_active=True).select_related('class_level__subject').order_by('class_level__subject__name', 'title')

        # Current filter values
        context['current_filters'] = {
            'subject': subject_filter,
            'level': level_filter,
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
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']

            try:
                # Read CSV content
                file_content = csv_file.read().decode('utf-8')

                # Import questions
                from core.utils.csv_import import CSVImporter
                importer = CSVImporter('questions', file_content, request.user)
                result = importer.import_data()

                if result['success']:
                    # Log successful import activity
                    AdminActivity.objects.create(
                        admin_user=request.user,
                        action='CSV_IMPORT',
                        description=f'Imported questions: {result["successful_rows"]} successful, {result["failed_rows"]} failed',
                        model_name='CSVImport',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )

                    if result["failed_rows"] > 0:
                        messages.warning(
                            request,
                            f'Import partially completed! {result["successful_rows"]} questions imported. '
                            f'{result["failed_rows"]} failed. Check the import log for details.'
                        )
                    else:
                        messages.success(
                            request,
                            f'Import completed successfully! {result["successful_rows"]} questions imported.'
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

        context = self.get_context_data(**kwargs)
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

            messages.success(request, 'Settings updated successfully!')
            return redirect('admin_panel:settings')

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

        # Get all levels for initial dropdown
        context['levels'] = ClassLevel.objects.filter(is_active=True).order_by('level_number')

        # Get selected filters from GET parameters
        level_id = self.request.GET.get('level_id')
        subject_id = self.request.GET.get('subject_id')
        topic_id = self.request.GET.get('topic_id')

        context['selected_level_id'] = level_id
        context['selected_subject_id'] = subject_id
        context['selected_topic_id'] = topic_id

        # Get subjects if level is selected
        if level_id:
            context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')

        # Get topics if subject is selected
        if subject_id:
            context['topics'] = Topic.objects.filter(
                subject_id=subject_id,
                is_active=True
            ).order_by('title')

        # Get study notes if topic is selected
        if topic_id:
            context['study_notes'] = StudyNote.objects.filter(
                topic_id=topic_id
            ).order_by('-created_at')

        return context


class CreateStudyNoteView(AdminRequiredMixin, View):
    """View for creating study notes"""

    def get(self, request):
        level_id = request.GET.get('level_id')
        subject_id = request.GET.get('subject_id')
        topic_id = request.GET.get('topic_id')

        context = {
            'levels': ClassLevel.objects.filter(is_active=True).order_by('level_number'),
            'selected_level_id': level_id,
            'selected_subject_id': subject_id,
            'selected_topic_id': topic_id,
        }

        if level_id:
            context['subjects'] = Subject.objects.filter(is_active=True).order_by('name')

        if subject_id:
            context['topics'] = Topic.objects.filter(
                subject_id=subject_id,
                is_active=True
            ).order_by('title')

        return render(request, 'admin_panel/create_study_note.html', context)

    def post(self, request):
        level_id = request.POST.get('level_id')
        subject_id = request.POST.get('subject_id')
        topic_id = request.POST.get('topic_id')
        topic_title = request.POST.get('topic_title', '').strip()
        note_title = request.POST.get('note_title', '').strip()
        content = request.POST.get('content', '').strip()

        if not all([level_id, subject_id, note_title, content]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect(f"{request.path}?level_id={level_id}&subject_id={subject_id}&topic_id={topic_id}")

        try:
            level = ClassLevel.objects.get(id=level_id, is_active=True)
            subject = Subject.objects.get(id=subject_id, is_active=True)

            # Create topic if it doesn't exist
            if topic_id:
                topic = Topic.objects.get(id=topic_id, is_active=True)
            elif topic_title:
                topic, created = Topic.objects.get_or_create(
                    title=topic_title,
                    subject=subject,
                    defaults={
                        'description': f'Study materials for {topic_title}',
                        'is_active': True
                    }
                )
                if created:
                    messages.success(request, f'Created new topic: {topic_title}')
            else:
                messages.error(request, 'Please select an existing topic or provide a title for a new topic.')
                return redirect(f"{request.path}?level_id={level_id}&subject_id={subject_id}")

            # Create study note
            study_note = StudyNote.objects.create(
                topic=topic,
                title=note_title,
                content=content,
                created_by=request.user
            )

            messages.success(request, f'Study note "{note_title}" created successfully!')
            return redirect(f'admin_panel:manage_study_notes?level_id={level_id}&subject_id={subject_id}&topic_id={topic.id}')

        except (ClassLevel.DoesNotExist, Subject.DoesNotExist, Topic.DoesNotExist):
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