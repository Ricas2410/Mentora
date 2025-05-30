from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, RedirectView
from django.http import JsonResponse
from django.views import View
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import Subject, ClassLevel, Topic
from content.models import StudyNote
from progress.models import UserProgress, StudyNoteProgress


class SubjectListView(TemplateView):
    template_name = 'subjects/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.filter(is_active=True).order_by('order')
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class SimpleLearnView(TemplateView):
    """
    Simplified learn page that shows subjects based on user's current class level
    Mobile-first, user-friendly approach for underprivileged learners
    """
    template_name = 'subjects/simple_learn.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            # Get user's current grade
            user_grade = self.request.user.current_class_level or 5

            # Get subjects available for user's current grade
            subjects = Subject.objects.filter(
                classlevels__level_number=user_grade,
                is_active=True
            ).distinct().order_by('order')

            # Get progress data for each subject
            subjects_with_progress = []
            completed_subjects = 0
            total_subjects = subjects.count()

            for subject in subjects:
                try:
                    # Get the class level for this subject and user's grade
                    class_level = ClassLevel.objects.get(
                        subject=subject,
                        level_number=user_grade,
                        is_active=True
                    )

                    # Get or create user progress for this subject
                    progress, created = UserProgress.objects.get_or_create(
                        user=self.request.user,
                        class_level=class_level,
                        defaults={'is_started': False}
                    )

                    # Update progress if needed
                    if created or progress.total_topics == 0:
                        progress.update_progress()

                    if progress.is_completed:
                        completed_subjects += 1

                    subjects_with_progress.append({
                        'subject': subject,
                        'progress': progress
                    })

                except ClassLevel.DoesNotExist:
                    # Subject doesn't have this grade level
                    continue

            # Calculate overall completion rate
            completion_rate = (completed_subjects / total_subjects * 100) if total_subjects > 0 else 0

            context.update({
                'subjects_with_progress': subjects_with_progress,
                'user_class_level': user_grade,
                'user_class_level_name': f'Grade {user_grade}',
                'completed_subjects': completed_subjects,
                'total_subjects': total_subjects,
                'completion_rate': completion_rate,
            })
        else:
            # For non-authenticated users, show all subjects without progress
            subjects = Subject.objects.filter(is_active=True).order_by('order')
            subjects_with_progress = []

            for subject in subjects:
                subjects_with_progress.append({
                    'subject': subject,
                    'progress': None
                })

            context.update({
                'subjects_with_progress': subjects_with_progress,
                'user_class_level_name': 'All Grades',
                'completed_subjects': 0,
                'total_subjects': subjects.count(),
                'completion_rate': 0,
            })

        return context


class SubjectRedirectView(RedirectView):
    """
    Smart redirect view that takes users directly to their current grade's topics
    for the selected subject, avoiding the unnecessary levels page
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        subject_id = kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id, is_active=True)

        # If user is authenticated, redirect to their current grade
        if self.request.user.is_authenticated:
            user_grade = self.request.user.current_class_level or 1

            try:
                # Find the class level for this subject and user's grade
                class_level = ClassLevel.objects.get(
                    subject=subject,
                    level_number=user_grade,
                    is_active=True
                )

                # Redirect directly to topics for their grade
                return reverse('subjects:topics', kwargs={
                    'subject_id': subject.id,
                    'level_id': class_level.id
                })

            except ClassLevel.DoesNotExist:
                # If no class level exists for user's grade, show all levels
                return reverse('subjects:levels', kwargs={'subject_id': subject.id})

        else:
            # For non-authenticated users, show all levels
            return reverse('subjects:levels', kwargs={'subject_id': subject.id})


class SubjectDetailView(TemplateView):
    template_name = 'subjects/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id, is_active=True)

        levels = subject.classlevels.filter(is_active=True).order_by('level_number')

        # Calculate total topics across all levels
        total_topics = sum(level.topics.filter(is_active=True).count() for level in levels)

        context['subject'] = subject
        context['levels'] = levels
        context['total_topics'] = total_topics
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class ClassLevelListView(TemplateView):
    template_name = 'subjects/levels.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = kwargs.get('subject_id')
        subject = get_object_or_404(Subject, id=subject_id, is_active=True)

        levels = subject.classlevels.filter(is_active=True).order_by('level_number')

        # Add progress data for authenticated users
        levels_with_progress = []
        if self.request.user.is_authenticated:
            from progress.models import UserProgress, TopicProgress

            for level in levels:
                # Get all topics for this level
                topics = level.topics.filter(is_active=True)
                total_topics = topics.count()

                if total_topics > 0:
                    # Count completed topics
                    completed_topics = TopicProgress.objects.filter(
                        user=self.request.user,
                        topic__in=topics,
                        is_completed=True
                    ).count()

                    # Calculate progress percentage
                    progress_percentage = int((completed_topics / total_topics) * 100) if total_topics > 0 else 0

                    # Check if level is completed (all topics completed)
                    is_completed = completed_topics == total_topics and total_topics > 0

                    # Check if level is unlocked (user's current level or below)
                    user_level = self.request.user.current_class_level or 1
                    is_unlocked = level.level_number <= user_level

                else:
                    completed_topics = 0
                    progress_percentage = 0
                    is_completed = False
                    is_unlocked = True

                levels_with_progress.append({
                    'level': level,
                    'total_topics': total_topics,
                    'completed_topics': completed_topics,
                    'progress_percentage': progress_percentage,
                    'is_completed': is_completed,
                    'is_unlocked': is_unlocked,
                })
        else:
            # For non-authenticated users, just add basic level info
            for level in levels:
                topics = level.topics.filter(is_active=True)
                levels_with_progress.append({
                    'level': level,
                    'total_topics': topics.count(),
                    'completed_topics': 0,
                    'progress_percentage': 0,
                    'is_completed': False,
                    'is_unlocked': True,
                })

        context['subject'] = subject
        context['levels'] = levels
        context['levels_with_progress'] = levels_with_progress
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class ClassLevelDetailView(TemplateView):
    template_name = 'subjects/level_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = kwargs.get('subject_id')
        level_id = kwargs.get('level_id')

        subject = get_object_or_404(Subject, id=subject_id, is_active=True)
        level = get_object_or_404(ClassLevel, id=level_id, subject=subject, is_active=True)

        topics = level.topics.filter(is_active=True).order_by('order')

        # Add progress data for authenticated users
        topics_with_progress = []
        if self.request.user.is_authenticated:
            from progress.models import TopicProgress

            for topic in topics:
                # Get topic progress
                try:
                    topic_progress = TopicProgress.objects.get(
                        user=self.request.user,
                        topic=topic
                    )
                    progress_percentage = int(topic_progress.progress_percentage) if topic_progress.progress_percentage else 0
                    is_completed = topic_progress.is_completed
                except TopicProgress.DoesNotExist:
                    progress_percentage = 0
                    is_completed = False

                topics_with_progress.append({
                    'topic': topic,
                    'progress_percentage': progress_percentage,
                    'is_completed': is_completed,
                })
        else:
            # For non-authenticated users, just add basic topic info
            for topic in topics:
                topics_with_progress.append({
                    'topic': topic,
                    'progress_percentage': 0,
                    'is_completed': False,
                })

        context['subject'] = subject
        context['level'] = level
        context['topics'] = topics
        context['topics_with_progress'] = topics_with_progress
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class TopicListView(TemplateView):
    template_name = 'subjects/topics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject_id = kwargs.get('subject_id')
        level_id = kwargs.get('level_id')

        subject = get_object_or_404(Subject, id=subject_id, is_active=True)
        level = get_object_or_404(ClassLevel, id=level_id, subject=subject, is_active=True)

        topics = level.topics.filter(is_active=True).order_by('order')

        # Add content availability information
        from content.models import Question, StudyNote

        # Add user progress data for authenticated users
        if self.request.user.is_authenticated:
            from progress.models import TopicProgress, UserProgress

            # Get user progress for each topic
            topics_with_progress = []
            completed_topics = 0
            total_duration = 0

            for topic in topics:
                # Check content availability
                has_questions = Question.objects.filter(topic=topic, is_active=True).exists()
                has_study_notes = StudyNote.objects.filter(topic=topic, is_active=True).exists()

                # Get or create topic progress
                try:
                    topic_progress = TopicProgress.objects.get(
                        user=self.request.user,
                        topic=topic
                    )
                except TopicProgress.DoesNotExist:
                    # Create a new progress object but don't save it yet
                    topic_progress = TopicProgress(
                        user=self.request.user,
                        topic=topic
                    )

                # All topics are available - no locking based on previous completion
                # Users can choose their own learning path
                is_available = True

                # Store progress data and content availability as attributes
                setattr(topic, 'topic_progress', topic_progress)
                setattr(topic, 'is_available', is_available)
                setattr(topic, 'has_questions', has_questions)
                setattr(topic, 'has_study_notes', has_study_notes)

                topics_with_progress.append({
                    'topic': topic,
                    'user_progress': topic_progress
                })

                if topic_progress.is_completed:
                    completed_topics += 1

                total_duration += topic.estimated_duration or 15

            # Calculate overall progress
            user_progress_percentage = (completed_topics / len(topics)) * 100 if topics else 0

            # Get or create class level progress
            try:
                class_progress = UserProgress.objects.get(
                    user=self.request.user,
                    class_level=level
                )
            except UserProgress.DoesNotExist:
                class_progress = UserProgress.objects.create(
                    user=self.request.user,
                    class_level=level
                )

            context['topics'] = [item['topic'] for item in topics_with_progress]
            context['completed_topics'] = completed_topics
            context['user_progress_percentage'] = user_progress_percentage
            context['total_duration'] = total_duration
            context['class_progress'] = class_progress
        else:
            # For non-authenticated users, just show topics without progress but with content availability
            for topic in topics:
                # Check content availability
                has_questions = Question.objects.filter(topic=topic, is_active=True).exists()
                has_study_notes = StudyNote.objects.filter(topic=topic, is_active=True).exists()

                setattr(topic, 'is_available', True)  # Show all as available for visitors
                setattr(topic, 'topic_progress', None)
                setattr(topic, 'has_questions', has_questions)
                setattr(topic, 'has_study_notes', has_study_notes)
            context['topics'] = topics
            context['completed_topics'] = 0
            context['user_progress_percentage'] = 0

        context['subject'] = subject
        context['level'] = level
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class TopicDetailView(TemplateView):
    template_name = 'subjects/topic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id = kwargs.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id, is_active=True)

        # Get study notes with progress information
        study_notes = topic.get_study_notes()
        notes_with_progress = []

        if self.request.user.is_authenticated:
            from progress.models import StudyNoteProgress

            for note in study_notes:
                try:
                    note_progress = StudyNoteProgress.objects.get(
                        user=self.request.user,
                        study_note=note
                    )
                    is_read = note_progress.is_read
                    read_at = note_progress.read_at
                except StudyNoteProgress.DoesNotExist:
                    is_read = False
                    read_at = None

                notes_with_progress.append({
                    'note': note,
                    'is_read': is_read,
                    'read_at': read_at
                })
        else:
            # For non-authenticated users, just add the notes without progress
            for note in study_notes:
                notes_with_progress.append({
                    'note': note,
                    'is_read': False,
                    'read_at': None
                })

        context['topic'] = topic
        context['subject'] = topic.class_level.subject
        context['level'] = topic.class_level
        context['notes_with_progress'] = notes_with_progress
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class QuizListView(TemplateView):
    """View to show available quizzes - subjects for user's current class"""
    template_name = 'subjects/quiz_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import Question

        # For authenticated users, show subjects for their current class level
        if self.request.user.is_authenticated:
            user_class_level = getattr(self.request.user, 'current_class_level', 1)

            # Get subjects that have class levels for the user's current grade
            subjects = Subject.objects.filter(
                is_active=True,
                classlevels__level_number=user_class_level,
                classlevels__is_active=True
            ).distinct().order_by('order')

            subjects_data = []
            for subject in subjects:
                try:
                    # Get the class level for this subject and user's grade
                    class_level = ClassLevel.objects.get(
                        subject=subject,
                        level_number=user_class_level,
                        is_active=True
                    )

                    # Count topics with questions for this subject/level
                    topics_with_questions = 0
                    total_questions = 0

                    completed_topics = 0

                    for topic in class_level.topics.filter(is_active=True):
                        question_count = Question.objects.filter(
                            topic=topic,
                            is_active=True
                        ).count()

                        if question_count > 0:
                            topics_with_questions += 1
                            total_questions += question_count

                            # Check if user has completed this topic (passed quiz)
                            from progress.models import TopicProgress
                            topic_progress = TopicProgress.objects.filter(
                                user=self.request.user,
                                topic=topic,
                                is_completed=True
                            ).first()

                            if topic_progress:
                                completed_topics += 1

                    # Only include subjects that have topics with questions
                    if topics_with_questions > 0:
                        # Calculate completion percentage
                        completion_percentage = (completed_topics / topics_with_questions) * 100 if topics_with_questions > 0 else 0

                        subjects_data.append({
                            'subject': subject,
                            'class_level': class_level,
                            'topics_with_questions': topics_with_questions,
                            'total_questions': total_questions,
                            'completed_topics': completed_topics,
                            'completion_percentage': round(completion_percentage, 1),
                            'is_completed': completion_percentage == 100,
                        })

                except ClassLevel.DoesNotExist:
                    # Subject doesn't have this grade level
                    continue

            # Sort subjects: incomplete first, then completed
            subjects_data.sort(key=lambda x: (x['is_completed'], -x['completion_percentage']))

            context['current_grade_subjects'] = subjects_data
            context['user_class_level'] = user_class_level
            context['user_class_level_name'] = f"Grade {user_class_level}"
        else:
            # For non-authenticated users, show a sample of available subjects
            context['current_grade_subjects'] = []
            context['user_class_level'] = None

        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class QuizTopicsView(TemplateView):
    """View to show quiz topics for a specific subject and grade"""
    template_name = 'subjects/quiz_topics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from content.models import Question

        grade_number = kwargs.get('grade_number')
        subject_id = kwargs.get('subject_id')

        # Get the subject and class level
        subject = get_object_or_404(Subject, id=subject_id, is_active=True)
        class_level = get_object_or_404(
            ClassLevel,
            subject=subject,
            level_number=grade_number,
            is_active=True
        )

        # Get topics with questions for this subject/level
        topics = class_level.topics.filter(is_active=True).order_by('order')

        topics_data = []
        for topic in topics:
            question_count = Question.objects.filter(
                topic=topic,
                is_active=True
            ).count()

            if question_count > 0:
                # Check if user has completed this topic and get progress details
                is_completed = False
                progress_percentage = 0
                best_score = 0
                attempts_count = 0

                if self.request.user.is_authenticated:
                    from progress.models import TopicProgress
                    topic_progress = TopicProgress.objects.filter(
                        user=self.request.user,
                        topic=topic
                    ).first()

                    if topic_progress:
                        is_completed = topic_progress.is_completed
                        best_score = topic_progress.best_quiz_score

                        # Calculate progress percentage based on completion status
                        if is_completed:
                            progress_percentage = 100
                        elif topic_progress.quiz_completed:
                            # Quiz attempted but not passed
                            progress_percentage = 50
                        elif topic_progress.is_started:
                            # Started but no quiz taken
                            progress_percentage = 25
                        else:
                            progress_percentage = 0

                topics_data.append({
                    'topic': topic,
                    'question_count': question_count,
                    'is_completed': is_completed,
                    'progress_percentage': progress_percentage,
                    'best_score': best_score,
                    'attempts_count': attempts_count,
                })

        # Sort topics: incomplete first, then completed
        topics_data.sort(key=lambda x: x['is_completed'])

        # Calculate completion status for final exam access
        completed_topics_count = sum(1 for topic_data in topics_data if topic_data['is_completed'])
        total_topics_count = len(topics_data)
        all_quizzes_completed = completed_topics_count == total_topics_count and total_topics_count > 0

        context['subject'] = subject
        context['class_level'] = class_level
        context['grade_number'] = grade_number
        context['quiz_topics'] = topics_data
        context['completed_topics_count'] = completed_topics_count
        context['total_topics_count'] = total_topics_count
        context['all_quizzes_completed'] = all_quizzes_completed
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class SubjectsByLevelAPIView(View):
    """API endpoint to get subjects available for a specific level"""

    def get(self, request, level_number):
        try:
            # Get subjects that have class levels for this level number
            subjects = Subject.objects.filter(
                is_active=True,
                classlevels__level_number=level_number,
                classlevels__is_active=True
            ).distinct().order_by('order')

            subjects_data = []
            for subject in subjects:
                subjects_data.append({
                    'id': str(subject.id),
                    'name': subject.name,
                    'description': subject.description,
                    'icon': subject.icon,
                    'color': subject.color
                })

            return JsonResponse({'subjects': subjects_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class QuizTopicsByLevelSubjectAPIView(View):
    """API endpoint to get quiz topics for a specific level and subject"""

    def get(self, request, level_number, subject_id):
        try:
            subject = get_object_or_404(Subject, id=subject_id, is_active=True)
            level = get_object_or_404(
                ClassLevel,
                subject=subject,
                level_number=level_number,
                is_active=True
            )

            from content.models import Question
            topics = level.topics.filter(is_active=True).order_by('order')

            topics_data = []
            for topic in topics:
                # Count active questions for this topic
                question_count = Question.objects.filter(
                    topic=topic,
                    is_active=True
                ).count()

                # Only include topics with questions
                if question_count > 0:
                    topics_data.append({
                        'id': str(topic.id),
                        'title': topic.title,
                        'description': topic.description,
                        'order': topic.order,
                        'estimated_duration': topic.estimated_duration,
                        'difficulty_level': topic.difficulty_level,
                        'question_count': question_count
                    })

            return JsonResponse({
                'topics': topics_data,
                'subject': {
                    'id': str(subject.id),
                    'name': subject.name
                },
                'level': {
                    'id': str(level.id),
                    'name': level.name,
                    'level_number': level.level_number
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class UserCurrentProgressAPIView(View):
    """API endpoint to get user's current progress"""

    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            from progress.models import UserProgress

            # Get user's current class level
            current_grade = request.user.current_class_level or 1

            # Get progress for current grade across all subjects
            progress_data = {
                'completed_subjects': 0,
                'total_subjects': 5,
                'completion_percentage': 0,
                'promotion_eligible': False
            }

            # Calculate actual progress
            subjects = Subject.objects.filter(is_active=True)
            total_subjects = subjects.count()
            completed_subjects = 0

            for subject in subjects:
                try:
                    class_level = ClassLevel.objects.get(
                        subject=subject,
                        level_number=current_grade,
                        is_active=True
                    )
                    user_progress = UserProgress.objects.get(
                        user=request.user,
                        class_level=class_level
                    )
                    if user_progress.is_completed:
                        completed_subjects += 1
                except (ClassLevel.DoesNotExist, UserProgress.DoesNotExist):
                    pass

            if total_subjects > 0:
                completion_percentage = (completed_subjects / total_subjects) * 100
                progress_data = {
                    'completed_subjects': completed_subjects,
                    'total_subjects': total_subjects,
                    'completion_percentage': completion_percentage,
                    'promotion_eligible': completion_percentage >= 80
                }

            return JsonResponse({
                'current_grade': current_grade,
                'progress_data': progress_data
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class UserGradeSubjectsAPIView(View):
    """API endpoint to get subjects for a specific grade with user progress"""

    def get(self, request, grade_number):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            from progress.models import UserProgress, TopicProgress

            # Get subjects that have class levels for this grade
            subjects = Subject.objects.filter(
                is_active=True,
                classlevels__level_number=grade_number,
                classlevels__is_active=True
            ).distinct().order_by('order')

            subjects_data = []
            for subject in subjects:
                try:
                    class_level = ClassLevel.objects.get(
                        subject=subject,
                        level_number=grade_number,
                        is_active=True
                    )

                    # Get user progress for this subject
                    try:
                        user_progress = UserProgress.objects.get(
                            user=request.user,
                            class_level=class_level
                        )
                        is_completed = user_progress.is_completed
                        progress_percentage = user_progress.completion_percentage
                    except UserProgress.DoesNotExist:
                        is_completed = False
                        progress_percentage = 0

                    # Count available topics
                    available_topics = class_level.topics.filter(is_active=True).count()

                    subjects_data.append({
                        'id': str(subject.id),
                        'name': subject.name,
                        'description': subject.description,
                        'icon': subject.icon,
                        'color': subject.color,
                        'is_completed': is_completed,
                        'progress_percentage': progress_percentage,
                        'available_topics': available_topics,
                        'class_level_id': str(class_level.id)
                    })

                except ClassLevel.DoesNotExist:
                    # Subject doesn't have this grade level
                    continue

            return JsonResponse({'subjects': subjects_data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class MarkNoteAsReadView(View):
    """API endpoint to mark a study note as read"""

    def post(self, request, note_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        try:
            import json
            from progress.models import StudyNoteProgress

            # Get the study note
            study_note = get_object_or_404(StudyNote, id=note_id, is_active=True)

            # Get or create progress record
            note_progress, created = StudyNoteProgress.objects.get_or_create(
                user=request.user,
                study_note=study_note
            )

            # Mark as read
            note_progress.mark_as_read()

            return JsonResponse({
                'success': True,
                'message': 'Note marked as read',
                'is_read': note_progress.is_read,
                'read_at': note_progress.read_at.isoformat() if note_progress.read_at else None
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class QuizTopicsWithProgressAPIView(View):
    """API endpoint to get quiz topics with user progress for a specific grade and subject"""

    def get(self, request, grade_number, subject_id):
        try:
            subject = get_object_or_404(Subject, id=subject_id, is_active=True)
            level = get_object_or_404(
                ClassLevel,
                subject=subject,
                level_number=grade_number,
                is_active=True
            )

            from content.models import Question
            from progress.models import TopicProgress

            topics = level.topics.filter(is_active=True).order_by('order')

            topics_data = []
            for topic in topics:
                # Count active questions for this topic
                question_count = Question.objects.filter(
                    topic=topic,
                    is_active=True
                ).count()

                # Only include topics with questions
                if question_count > 0:
                    # Get user progress if authenticated
                    is_completed = False
                    progress_percentage = 0

                    if request.user.is_authenticated:
                        try:
                            topic_progress = TopicProgress.objects.get(
                                user=request.user,
                                topic=topic
                            )
                            is_completed = topic_progress.is_completed
                            progress_percentage = topic_progress.completion_percentage
                        except TopicProgress.DoesNotExist:
                            pass

                    topics_data.append({
                        'id': str(topic.id),
                        'title': topic.title,
                        'description': topic.description,
                        'order': topic.order,
                        'estimated_duration': topic.estimated_duration,
                        'difficulty_level': topic.difficulty_level,
                        'question_count': question_count,
                        'is_completed': is_completed,
                        'progress_percentage': progress_percentage
                    })

            return JsonResponse({
                'topics': topics_data,
                'subject': {
                    'id': str(subject.id),
                    'name': subject.name
                },
                'level': {
                    'id': str(level.id),
                    'name': level.name,
                    'level_number': level.level_number
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
