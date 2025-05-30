import random
import time
from typing import List, Dict, Any
from django.db.models import QuerySet
from .models import Question, AnswerChoice


def generate_quiz_questions(topic, max_questions: int = 10, user_id: str = None) -> Dict[str, Any]:
    """
    Generate shuffled quiz questions for a topic with intelligent question selection.
    Handles both regular questions and comprehension passages.

    Args:
        topic: Topic instance
        max_questions: Maximum number of questions to include
        user_id: User ID for personalized question selection

    Returns:
        Dictionary containing shuffled questions and metadata
    """
    from .models import Passage

    # Check if topic has comprehension passages
    passages = Passage.objects.filter(topic=topic, is_active=True).prefetch_related('questions__answer_choices')

    if passages.exists():
        # Handle comprehension quiz
        return generate_comprehension_quiz(topic, passages, max_questions, user_id)
    else:
        # Handle regular quiz
        return generate_regular_quiz(topic, max_questions, user_id)


def generate_comprehension_quiz(topic, passages, max_questions: int = 10, user_id: str = None) -> Dict[str, Any]:
    """
    Generate a comprehension quiz with one passage and its questions.
    """
    seed = int(time.time()) + hash(str(user_id)) if user_id else int(time.time())
    random.seed(seed)

    # Select a random passage
    selected_passage = random.choice(list(passages))

    # Get questions for this passage
    passage_questions = selected_passage.get_random_questions(max_questions)

    if not passage_questions:
        return {
            'questions': [],
            'total_questions': 0,
            'total_available': 0,
            'shuffled': False,
            'seed': seed,
            'question_ids': [],
            'passage': None,
            'is_comprehension': True
        }

    # Shuffle the selected questions
    random.shuffle(passage_questions)

    # Prepare question data
    shuffled_questions = []
    question_ids = []

    for question in passage_questions:
        # Get answer choices and shuffle them
        choices = list(question.answer_choices.all())
        random.shuffle(choices)

        # Create question data with shuffled choices
        question_data = {
            'id': str(question.id),
            'question_text': question.question_text,
            'question_type': question.question_type,
            'correct_answer': question.correct_answer,
            'acceptable_answers': question.get_acceptable_answers_list(),
            'explanation': question.explanation,
            'time_limit': question.time_limit,
            'explanation_display_time': question.explanation_display_time,
            'choices': [
                {
                    'id': str(choice.id),
                    'text': choice.choice_text,
                    'isCorrect': choice.is_correct,
                    'order': choice.order
                }
                for choice in choices
            ]
        }

        shuffled_questions.append(question_data)
        question_ids.append(str(question.id))

    # Prepare passage data
    passage_data = {
        'id': str(selected_passage.id),
        'title': selected_passage.title,
        'content': selected_passage.content,
        'passage_type': selected_passage.passage_type,
        'author': selected_passage.author,
        'estimated_reading_time': selected_passage.estimated_reading_time
    }

    return {
        'questions': shuffled_questions,
        'total_questions': len(shuffled_questions),
        'total_available': selected_passage.get_questions().count(),
        'shuffled': True,
        'seed': seed,
        'question_ids': question_ids,
        'passage': passage_data,
        'is_comprehension': True
    }


def generate_regular_quiz(topic, max_questions: int = 10, user_id: str = None) -> Dict[str, Any]:
    """
    Generate a regular quiz with mixed questions from the topic.
    """
    # Get all active questions for the topic (excluding passage-based questions)
    all_questions = Question.objects.filter(
        topic=topic,
        is_active=True,
        passage__isnull=True  # Exclude comprehension questions
    ).prefetch_related('answer_choices')

    total_available = all_questions.count()

    if total_available == 0:
        return {
            'questions': [],
            'total_questions': 0,
            'total_available': 0,
            'shuffled': False,
            'seed': 0,
            'question_ids': [],
            'passage': None,
            'is_comprehension': False
        }

    # Limit questions to available count
    actual_questions = min(max_questions, total_available)

    # Create a seed for consistent shuffling within the same session
    seed = int(time.time()) + hash(str(user_id)) if user_id else int(time.time())
    random.seed(seed)

    # Convert to list and shuffle
    questions_list = list(all_questions)
    random.shuffle(questions_list)

    # Take the required number of questions
    selected_questions = questions_list[:actual_questions]

    # Prepare shuffled questions data
    shuffled_questions = []
    question_ids = []

    for question in selected_questions:
        # Get answer choices and shuffle them
        choices = list(question.answer_choices.all())
        random.shuffle(choices)

        # Create question data with shuffled choices
        question_data = {
            'id': str(question.id),
            'question_text': question.question_text,
            'question_type': question.question_type,
            'correct_answer': question.correct_answer,
            'acceptable_answers': question.get_acceptable_answers_list(),
            'explanation': question.explanation,
            'time_limit': question.time_limit,
            'explanation_display_time': question.explanation_display_time,
            'choices': [
                {
                    'id': str(choice.id),
                    'text': choice.choice_text,
                    'isCorrect': choice.is_correct,
                    'order': choice.order
                }
                for choice in choices
            ]
        }

        shuffled_questions.append(question_data)
        question_ids.append(str(question.id))

    return {
        'questions': shuffled_questions,
        'total_questions': len(shuffled_questions),
        'total_available': total_available,
        'shuffled': True,
        'seed': seed,
        'question_ids': question_ids,
        'passage': None,
        'is_comprehension': False
    }


def get_quiz_statistics(topic) -> Dict[str, int]:
    """
    Get statistics about questions available for a topic.

    Args:
        topic: Topic object

    Returns:
        Dict with question statistics
    """
    questions = Question.objects.filter(topic=topic, is_active=True)

    return {
        'total_questions': questions.count(),
        'easy_questions': questions.filter(difficulty='easy').count(),
        'medium_questions': questions.filter(difficulty='medium').count(),
        'hard_questions': questions.filter(difficulty='hard').count(),
        'multiple_choice': questions.filter(question_type='multiple_choice').count(),
        'fill_blank': questions.filter(question_type='fill_blank').count(),
        'true_false': questions.filter(question_type='true_false').count(),
    }


def get_user_quiz_attempts(user, topic) -> int:
    """
    Get the number of quiz attempts a user has made for a topic.

    Args:
        user: User object
        topic: Topic object

    Returns:
        Number of attempts
    """
    from .models import Quiz
    return Quiz.objects.filter(user=user, topic=topic).count()


def calculate_recommended_questions(total_available: int) -> int:
    """
    Calculate recommended number of questions based on available questions.

    Args:
        total_available: Total number of questions available

    Returns:
        Recommended number of questions for quiz
    """
    if total_available <= 5:
        return total_available
    elif total_available <= 10:
        return min(8, total_available)
    elif total_available <= 20:
        return 10
    elif total_available <= 50:
        return 15
    else:
        return 20
