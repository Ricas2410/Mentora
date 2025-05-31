from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from subjects.models import Topic
from .models import Question, Quiz, QuizAnswer, Test, TestAnswer, AnswerChoice
from .utils import generate_quiz_questions, get_quiz_statistics, get_user_quiz_attempts, calculate_recommended_questions
from admin_panel.utils import get_quiz_settings


class StudyNotesView(TemplateView):
    template_name = 'content/study_notes.html'


class QuizView(TemplateView):
    template_name = 'content/quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_id = kwargs.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id, is_active=True)

        # Get quiz settings from admin
        quiz_settings = get_quiz_settings()

        # Get quiz statistics
        stats = get_quiz_statistics(topic)
        total_available = stats['total_questions']

        # Use admin settings for number of questions, fallback to calculated
        recommended_questions = min(quiz_settings['quiz_questions_per_topic'], total_available) if total_available > 0 else quiz_settings['quiz_questions_per_topic']

        # Generate shuffled questions for this quiz attempt
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        quiz_data = generate_quiz_questions(
            topic=topic,
            max_questions=recommended_questions,
            user_id=user_id
        )

        # Get user's attempt count
        attempt_count = 0
        user_progress = None
        current_class_subjects = []
        progress_summary = None

        if self.request.user.is_authenticated:
            attempt_count = get_user_quiz_attempts(self.request.user, topic)

            # Get user progress information
            from progress.models import UserProgress
            try:
                user_progress = UserProgress.objects.get(
                    user=self.request.user,
                    class_level=topic.class_level
                )

                # Get all subjects for current class level
                from subjects.models import ClassLevel
                current_class_subjects = ClassLevel.objects.filter(
                    level_number=topic.class_level.level_number,
                    is_active=True
                ).select_related('subject')

                # Get progress summary
                progress_summary = {
                    'completion_percentage': user_progress.completion_percentage,
                    'topics_completed': user_progress.topics_completed,
                    'total_topics': user_progress.total_topics,
                    'current_class': topic.class_level.name
                }

            except UserProgress.DoesNotExist:
                # Create progress record if it doesn't exist
                user_progress = UserProgress.objects.create(
                    user=self.request.user,
                    class_level=topic.class_level,
                    is_started=True
                )

                # Get subjects for current class level
                from subjects.models import ClassLevel
                current_class_subjects = ClassLevel.objects.filter(
                    level_number=topic.class_level.level_number,
                    is_active=True
                ).select_related('subject')

                # Initialize progress summary for new user
                progress_summary = {
                    'completion_percentage': 0,
                    'topics_completed': 0,
                    'total_topics': topic.class_level.topics.filter(is_active=True).count(),
                    'current_class': topic.class_level.name
                }

        # Create quiz info for the template using admin settings
        quiz_info = {
            'title': f"{topic.title} Quiz",
            'description': f"Test your knowledge of {topic.title}",
            'time_limit': quiz_settings['quiz_time_limit'],  # Use admin setting
            'question_time_limit': quiz_settings['question_time_limit'],  # Individual question time
            'explanation_display_time': quiz_settings.get('explanation_display_time', 5),  # Explanation time
            'questions_count': quiz_data['total_questions'],
            'has_questions': quiz_data['total_questions'] > 0,
            'total_available': total_available,
            'is_shuffled': quiz_data['shuffled'] and quiz_settings['shuffle_questions'],  # Use admin setting
            'shuffle_answers': quiz_settings['shuffle_answers'],  # Answer shuffling
            'show_correct_answers': quiz_settings['show_correct_answers'],
            'allow_question_skip': quiz_settings['allow_question_skip'],
            'show_progress_bar': quiz_settings['show_progress_bar'],
            'minimum_pass_percentage': quiz_settings['minimum_pass_percentage'],
            'attempt_number': attempt_count + 1,
            'seed': quiz_data['seed'],
            'is_comprehension': quiz_data.get('is_comprehension', False),
            'passage': quiz_data.get('passage')
        }

        # Prepare JSON data for JavaScript
        questions_data = []
        for question in quiz_data['questions']:
            question_data = {
                'id': question['id'],
                'text': question['question_text'],
                'type': question['question_type'],
                'correctAnswer': question['correct_answer'],
                'explanation': question['explanation'],
                'timeLimit': question['time_limit'],
                'choices': []
            }

            # Add choices for multiple choice questions
            if question['question_type'] == 'multiple_choice':
                for choice in question['choices']:
                    question_data['choices'].append({
                        'id': choice['id'],
                        'text': choice['text'],
                        'isCorrect': choice['isCorrect']
                    })

            questions_data.append(question_data)

        quiz_metadata = {
            'isShuffled': quiz_info['is_shuffled'],
            'attemptNumber': quiz_info['attempt_number'],
            'totalAvailable': quiz_info['total_available'],
            'seed': quiz_info['seed'],
            'isUserAuthenticated': self.request.user.is_authenticated
        }

        context['topic'] = topic
        context['subject'] = topic.class_level.subject
        context['level'] = topic.class_level
        context['quiz_info'] = quiz_info
        context['questions'] = quiz_data['questions']
        context['questions_json'] = json.dumps(questions_data)
        context['quiz_metadata_json'] = json.dumps(quiz_metadata)
        context['quiz_stats'] = stats
        context['show_login_prompt'] = not self.request.user.is_authenticated
        context['user_progress'] = user_progress
        context['current_class_subjects'] = current_class_subjects
        context['progress_summary'] = progress_summary
        return context


class TakeQuizView(TemplateView):
    template_name = 'content/take_quiz.html'


class QuizResultView(TemplateView):
    template_name = 'content/quiz_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz_id = kwargs.get('quiz_id')

        # Get topic from quiz_id (which is actually topic_id in our URL pattern)
        topic = get_object_or_404(Topic, id=quiz_id, is_active=True)

        context['topic'] = topic
        context['subject'] = topic.class_level.subject
        context['level'] = topic.class_level
        return context


class TestView(TemplateView):
    template_name = 'content/test.html'


class TakeTestView(TemplateView):
    template_name = 'content/take_test.html'


class TestResultView(TemplateView):
    template_name = 'content/test_result.html'


class ExamView(TemplateView):
    template_name = 'content/exam.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level_id = kwargs.get('level_id')

        from subjects.models import ClassLevel
        from admin_panel.utils import get_quiz_settings

        level = get_object_or_404(ClassLevel, id=level_id, is_active=True)
        topics = level.topics.filter(is_active=True).order_by('order')

        # Get exam settings
        settings = get_quiz_settings()
        exam_questions_per_level = settings.get('exam_questions_per_level', 30)
        exam_time_limit = settings.get('exam_time_limit', 3600)  # seconds
        pass_percentage = settings.get('minimum_pass_percentage', 60)

        # Count total available questions across all topics
        total_available_questions = Question.objects.filter(
            topic__in=topics,
            is_active=True
        ).count()

        # Determine actual number of questions for exam
        if total_available_questions < exam_questions_per_level:
            total_questions = total_available_questions
            insufficient_questions = True
        else:
            total_questions = exam_questions_per_level
            insufficient_questions = False

        context['level'] = level
        context['subject'] = level.subject
        context['topics'] = topics
        context['total_questions'] = total_questions
        context['exam_time_limit'] = exam_time_limit // 60  # Convert to minutes
        context['pass_percentage'] = pass_percentage
        context['insufficient_questions'] = insufficient_questions
        context['show_login_prompt'] = not self.request.user.is_authenticated
        return context


class TakeExamView(TemplateView):
    template_name = 'content/take_exam.html'

    def dispatch(self, request, *args, **kwargs):
        # Require authentication for taking exams
        if not request.user.is_authenticated:
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        level_id = kwargs.get('level_id')

        from subjects.models import ClassLevel
        from admin_panel.utils import get_quiz_settings
        import random

        level = get_object_or_404(ClassLevel, id=level_id, is_active=True)
        topics = level.topics.filter(is_active=True).order_by('order')

        # Get exam settings
        settings = get_quiz_settings()
        exam_questions_per_level = settings.get('exam_questions_per_level', 30)
        exam_time_limit = settings.get('exam_time_limit', 3600)  # seconds
        pass_percentage = settings.get('minimum_pass_percentage', 60)

        # Get all questions from all topics in this level
        all_questions = Question.objects.filter(
            topic__in=topics,
            is_active=True
        ).order_by('?')  # Random order

        # Determine number of questions to use
        total_available = all_questions.count()
        if total_available < exam_questions_per_level:
            questions_to_use = total_available
        else:
            questions_to_use = exam_questions_per_level

        # Get the questions for this exam
        exam_questions = list(all_questions[:questions_to_use])

        # Shuffle questions
        random.shuffle(exam_questions)

        # Create exam record
        exam = Test.objects.create(
            class_level=level,
            user=self.request.user,
            test_type='level_exam',
            total_questions=questions_to_use,
            time_limit=exam_time_limit,
            pass_percentage=pass_percentage
        )

        # Prepare questions data for frontend
        questions_data = []
        for i, question in enumerate(exam_questions):
            question_data = {
                'id': str(question.id),
                'question_text': question.question_text,
                'question_type': question.question_type,
                'order': i + 1,
                'points': question.points,
                'time_limit': question.time_limit,
            }

            # Add choices for multiple choice questions
            if question.question_type == 'multiple_choice':
                choices = question.answer_choices.all().order_by('order')
                question_data['choices'] = [
                    {
                        'id': str(choice.id),
                        'text': choice.choice_text,
                        'order': choice.order
                    }
                    for choice in choices
                ]

            questions_data.append(question_data)

        context['level'] = level
        context['subject'] = level.subject
        context['exam'] = exam
        context['questions'] = questions_data
        context['questions_json'] = json.dumps(questions_data)
        context['exam_time_limit'] = exam_time_limit
        context['total_questions'] = questions_to_use
        context['pass_percentage'] = pass_percentage
        return context


class ExamResultView(TemplateView):
    template_name = 'content/exam_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_id = kwargs.get('exam_id')

        exam = get_object_or_404(Test, id=exam_id, user=self.request.user)

        context['exam'] = exam
        context['level'] = exam.class_level
        context['subject'] = exam.class_level.subject
        return context


@csrf_exempt
@require_http_methods(["POST"])
def validate_text_answer(request):
    """
    API endpoint to validate text-based answers with intelligent matching.
    """
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        user_answer = data.get('user_answer', '').strip()

        if not question_id:
            return JsonResponse({
                'success': False,
                'error': 'Question ID is required'
            }, status=400)

        # Get the question
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Question not found'
            }, status=404)

        # Validate the answer using the model method
        is_correct, match_type, matched_answer = question.validate_text_answer(user_answer)

        # Prepare response data
        response_data = {
            'success': True,
            'is_correct': is_correct,
            'match_type': match_type,
            'user_answer': user_answer,
            'matched_answer': matched_answer,
            'acceptable_answers': question.get_acceptable_answers_list(),
            'explanation': question.explanation
        }

        # Add feedback message based on match type
        if is_correct:
            if match_type == 'exact':
                response_data['feedback'] = 'Perfect! Exact match.'
            elif match_type == 'similar':
                response_data['feedback'] = f'Correct! Your answer "{user_answer}" is very close to "{matched_answer}".'
            elif match_type == 'partial':
                response_data['feedback'] = f'Correct! Your answer "{user_answer}" matches "{matched_answer}".'
            elif match_type == 'word_match':
                response_data['feedback'] = f'Correct! Your answer contains the key words from "{matched_answer}".'
        else:
            if match_type == 'empty':
                response_data['feedback'] = 'Please provide an answer.'
            else:
                acceptable_list = ', '.join(question.get_acceptable_answers_list())
                response_data['feedback'] = f'Not quite right. Acceptable answers include: {acceptable_list}'

        return JsonResponse(response_data)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def submit_quiz(request):
    """Handle quiz submission and update progress"""
    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')
        answers = data.get('answers', {})
        time_taken = data.get('time_taken', 0)

        # Get topic
        topic = get_object_or_404(Topic, id=topic_id, is_active=True)

        # Get questions for this topic
        questions = Question.objects.filter(topic=topic, is_active=True)

        # Calculate score
        correct_answers = 0
        total_questions = len(answers)
        quiz_answers_data = []

        for question_id, user_answer in answers.items():
            try:
                question = questions.get(id=question_id)

                # Check if answer is correct
                if question.question_type == 'multiple_choice':
                    correct_choice = question.answer_choices.filter(is_correct=True).first()
                    is_correct = correct_choice and user_answer == correct_choice.choice_text
                else:
                    # For text-based questions
                    is_correct, _, _ = question.validate_text_answer(user_answer)

                if is_correct:
                    correct_answers += 1

                quiz_answers_data.append({
                    'question': question,
                    'user_answer': user_answer,
                    'is_correct': is_correct
                })

            except Question.DoesNotExist:
                continue

        # Calculate percentage
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        # Get current attempt number
        attempt_number = Quiz.objects.filter(user=request.user, topic=topic).count() + 1

        # Create quiz record
        quiz = Quiz.objects.create(
            topic=topic,
            user=request.user,
            total_questions=total_questions,
            score=correct_answers,
            total_points=total_questions,
            percentage=percentage,
            attempt_number=attempt_number,
            is_completed=True,
            completed_at=timezone.now()
        )

        # Create quiz answers
        for answer_data in quiz_answers_data:
            QuizAnswer.objects.create(
                quiz=quiz,
                question=answer_data['question'],
                user_answer=answer_data['user_answer'],
                is_correct=answer_data['is_correct'],
                points_earned=1 if answer_data['is_correct'] else 0
            )

        # Update topic progress
        from progress.models import TopicProgress, UserProgress

        topic_progress, created = TopicProgress.objects.get_or_create(
            user=request.user,
            topic=topic,
            defaults={
                'is_started': True,
                'started_at': timezone.now()
            }
        )

        # Update quiz score (only if better than previous)
        topic_progress.update_quiz_score(percentage)

        # Get quiz settings for passing score
        quiz_settings = get_quiz_settings()
        passing_score = quiz_settings['minimum_pass_percentage']

        # Update class level progress
        try:
            class_progress = UserProgress.objects.get(
                user=request.user,
                class_level=topic.class_level
            )
            class_progress.update_progress()
        except UserProgress.DoesNotExist:
            # Create class progress if it doesn't exist
            class_progress = UserProgress.objects.create(
                user=request.user,
                class_level=topic.class_level,
                is_started=True,
                started_at=timezone.now()
            )
            class_progress.update_progress()

        # Check for grade promotion
        check_grade_promotion(request.user)

        return JsonResponse({
            'success': True,
            'quiz_id': str(quiz.id),
            'score': correct_answers,
            'total': total_questions,
            'percentage': round(percentage, 1),
            'passed': percentage >= passing_score,
            'attempt_number': attempt_number,
            'topic_completed': topic_progress.is_completed
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def check_grade_promotion(user):
    """Check if user should be promoted to next grade"""
    from progress.models import UserProgress
    from subjects.models import ClassLevel, Subject

    # Get user's current grade
    current_grade = user.current_class_level or 1

    # Get all subjects for current grade
    current_grade_subjects = Subject.objects.filter(
        classlevels__level_number=current_grade,
        is_active=True
    ).distinct()

    # Check if all subjects are completed
    all_subjects_completed = True
    for subject in current_grade_subjects:
        try:
            class_level = ClassLevel.objects.get(
                subject=subject,
                level_number=current_grade
            )
            progress = UserProgress.objects.get(
                user=user,
                class_level=class_level
            )
            if not progress.is_completed:
                all_subjects_completed = False
                break
        except (ClassLevel.DoesNotExist, UserProgress.DoesNotExist):
            all_subjects_completed = False
            break

    # Promote user if all subjects completed
    if all_subjects_completed and current_grade < 12:
        user.current_class_level = current_grade + 1
        user.save()

        # Create progress records for next grade
        next_grade_subjects = Subject.objects.filter(
            classlevels__level_number=current_grade + 1,
            is_active=True
        ).distinct()

        for subject in next_grade_subjects:
            try:
                class_level = ClassLevel.objects.get(
                    subject=subject,
                    level_number=current_grade + 1
                )
                UserProgress.objects.get_or_create(
                    user=user,
                    class_level=class_level,
                    defaults={
                        'is_started': False
                    }
                )
            except ClassLevel.DoesNotExist:
                continue


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def get_next_learning_path(request):
    """Get the next learning path for the user after completing a topic"""
    try:
        data = json.loads(request.body)
        current_topic_id = data.get('current_topic_id')
        current_subject_id = data.get('current_subject_id')
        current_level_id = data.get('current_level_id')

        if not all([current_topic_id, current_subject_id, current_level_id]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required parameters'
            }, status=400)

        from subjects.models import Topic, ClassLevel, Subject
        from progress.models import TopicProgress, UserProgress
        from django.urls import reverse

        # Get current objects
        current_topic = get_object_or_404(Topic, id=current_topic_id)
        current_subject = get_object_or_404(Subject, id=current_subject_id)
        current_level = get_object_or_404(ClassLevel, id=current_level_id)

        # 1. Check for next topic in same subject
        next_topic = Topic.objects.filter(
            class_level=current_level,
            order__gt=current_topic.order,
            is_active=True
        ).order_by('order').first()

        if next_topic:
            # Check if next topic is unlocked
            try:
                topic_progress = TopicProgress.objects.get(
                    user=request.user,
                    topic=next_topic
                )
                if not topic_progress.is_locked:
                    return JsonResponse({
                        'success': True,
                        'next_path': {
                            'type': 'next_topic',
                            'title': next_topic.title,
                            'url': reverse('subjects:topic_detail', args=[
                                current_subject.id, current_level.id, next_topic.id
                            ])
                        }
                    })
            except TopicProgress.DoesNotExist:
                # Topic not started yet, it's available
                return JsonResponse({
                    'success': True,
                    'next_path': {
                        'type': 'next_topic',
                        'title': next_topic.title,
                        'url': reverse('subjects:topic_detail', args=[
                            current_subject.id, current_level.id, next_topic.id
                        ])
                    }
                })

        # 2. Check for next subject in same grade
        current_grade = current_level.level_number
        next_subject = Subject.objects.filter(
            classlevels__level_number=current_grade,
            order__gt=current_subject.order,
            is_active=True
        ).order_by('order').first()

        if next_subject:
            try:
                next_level = ClassLevel.objects.get(
                    subject=next_subject,
                    level_number=current_grade
                )
                first_topic = Topic.objects.filter(
                    class_level=next_level,
                    is_active=True
                ).order_by('order').first()

                if first_topic:
                    return JsonResponse({
                        'success': True,
                        'next_path': {
                            'type': 'next_subject',
                            'title': next_subject.name,
                            'url': reverse('subjects:topic_detail', args=[
                                next_subject.id, next_level.id, first_topic.id
                            ])
                        }
                    })
            except ClassLevel.DoesNotExist:
                pass

        # 3. Check for grade promotion
        # First check if current grade is completed
        current_grade_subjects = Subject.objects.filter(
            classlevels__level_number=current_grade,
            is_active=True
        ).distinct()

        all_subjects_completed = True
        for subject in current_grade_subjects:
            try:
                class_level = ClassLevel.objects.get(
                    subject=subject,
                    level_number=current_grade
                )
                progress = UserProgress.objects.get(
                    user=request.user,
                    class_level=class_level
                )
                if not progress.is_completed:
                    all_subjects_completed = False
                    break
            except (ClassLevel.DoesNotExist, UserProgress.DoesNotExist):
                all_subjects_completed = False
                break

        if all_subjects_completed and current_grade < 12:
            # Promote user
            request.user.current_class_level = current_grade + 1
            request.user.save()

            # Get first subject of next grade
            next_grade_subject = Subject.objects.filter(
                classlevels__level_number=current_grade + 1,
                is_active=True
            ).order_by('order').first()

            if next_grade_subject:
                try:
                    next_grade_level = ClassLevel.objects.get(
                        subject=next_grade_subject,
                        level_number=current_grade + 1
                    )
                    first_topic = Topic.objects.filter(
                        class_level=next_grade_level,
                        is_active=True
                    ).order_by('order').first()

                    if first_topic:
                        return JsonResponse({
                            'success': True,
                            'next_path': {
                                'type': 'next_level',
                                'title': next_grade_subject.name,
                                'level_number': current_grade + 1,
                                'url': reverse('subjects:topic_detail', args=[
                                    next_grade_subject.id, next_grade_level.id, first_topic.id
                                ])
                            }
                        })
                except ClassLevel.DoesNotExist:
                    pass

        # 4. All completed
        if current_grade >= 12:
            return JsonResponse({
                'success': True,
                'next_path': {
                    'type': 'completed',
                    'title': 'All Grades Completed!',
                    'url': reverse('core:dashboard')
                }
            })

        # 5. Fallback - back to dashboard
        return JsonResponse({
            'success': True,
            'next_path': {
                'type': 'dashboard',
                'title': 'Continue Learning',
                'url': reverse('core:dashboard')
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_exam(request):
    """
    API endpoint to submit exam answers and calculate results
    """
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)

    try:
        data = json.loads(request.body)
        exam_id = data.get('exam_id')
        answers = data.get('answers', {})
        time_taken = data.get('time_taken', 0)

        # Get exam
        exam = get_object_or_404(Test, id=exam_id, user=request.user)

        if exam.is_completed:
            return JsonResponse({'success': False, 'message': 'Exam already completed'}, status=400)

        # Get all questions for this exam
        level = exam.class_level
        topics = level.topics.filter(is_active=True)
        all_questions = Question.objects.filter(topic__in=topics, is_active=True)

        # Process answers
        correct_answers = 0
        total_questions = len(answers)
        exam_answers_data = []

        for question_id, user_answer in answers.items():
            try:
                question = all_questions.get(id=question_id)

                # Validate answer
                is_correct = False
                if question.question_type == 'multiple_choice':
                    # For multiple choice, check if selected choice is correct
                    try:
                        selected_choice = AnswerChoice.objects.get(id=user_answer, question=question)
                        is_correct = selected_choice.is_correct
                    except AnswerChoice.DoesNotExist:
                        is_correct = False
                elif question.question_type in ['fill_blank', 'short_answer']:
                    # For text answers, use intelligent matching
                    correct_answers_list = [ans.strip().lower() for ans in question.correct_answer.split(',')]
                    user_answer_clean = user_answer.strip().lower()
                    is_correct = user_answer_clean in correct_answers_list
                elif question.question_type == 'true_false':
                    is_correct = user_answer.lower() == question.correct_answer.lower()

                if is_correct:
                    correct_answers += 1

                exam_answers_data.append({
                    'question': question,
                    'user_answer': user_answer,
                    'is_correct': is_correct
                })

            except Question.DoesNotExist:
                continue

        # Calculate percentage
        percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0

        # Update exam record
        exam.score = correct_answers
        exam.total_points = total_questions
        exam.percentage = percentage
        exam.passed = percentage >= exam.pass_percentage
        exam.is_completed = True
        exam.completed_at = timezone.now()
        exam.save()

        # Create exam answers
        for answer_data in exam_answers_data:
            TestAnswer.objects.create(
                test=exam,
                question=answer_data['question'],
                user_answer=answer_data['user_answer'],
                is_correct=answer_data['is_correct'],
                points_earned=1 if answer_data['is_correct'] else 0
            )

        # Update user progress if exam passed
        if exam.passed:
            from progress.models import UserProgress
            user_progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                class_level=level,
                defaults={
                    'is_completed': True,
                    'completed_at': timezone.now(),
                    'final_score': percentage,
                    'passed': True
                }
            )
            if not created and not user_progress.is_completed:
                user_progress.is_completed = True
                user_progress.completed_at = timezone.now()
                user_progress.final_score = max(user_progress.final_score, percentage)
                user_progress.passed = True
                user_progress.save()

        return JsonResponse({
            'success': True,
            'message': 'Exam submitted successfully',
            'exam_id': str(exam.id),
            'score': correct_answers,
            'total': total_questions,
            'percentage': percentage,
            'passed': exam.passed,
            'pass_percentage': exam.pass_percentage
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error submitting exam: {str(e)}'
        }, status=500)