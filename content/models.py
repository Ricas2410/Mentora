from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import json


class StudyNote(models.Model):
    """
    Model for study notes/content for each topic
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='study_notes')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Main study content in markdown or HTML")

    # Media attachments
    image = models.ImageField(upload_to='study_notes/images/', null=True, blank=True)
    audio_file = models.FileField(upload_to='study_notes/audio/', null=True, blank=True)
    video_url = models.URLField(blank=True, help_text="YouTube or other video URL")

    # Organization
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'study_notes'
        verbose_name = 'Study Note'
        verbose_name_plural = 'Study Notes'
        ordering = ['topic', 'order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class Passage(models.Model):
    """
    Model for reading comprehension passages
    """
    PASSAGE_TYPES = [
        ('story', 'Story'),
        ('article', 'Article'),
        ('poem', 'Poem'),
        ('dialogue', 'Dialogue'),
        ('informational', 'Informational Text'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='passages')
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="The reading passage content")
    passage_type = models.CharField(max_length=20, choices=PASSAGE_TYPES, default='story')

    # Metadata
    author = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=200, blank=True)
    reading_level = models.CharField(max_length=20, blank=True, help_text="Grade level or difficulty")
    estimated_reading_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")

    # Settings
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'passages'
        verbose_name = 'Reading Passage'
        verbose_name_plural = 'Reading Passages'
        ordering = ['topic', 'order', 'title']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

    def get_questions(self):
        """Get all questions for this passage"""
        return self.questions.filter(is_active=True).order_by('order', 'created_at')

    def get_random_questions(self, count=10):
        """Get random questions for this passage"""
        import random
        questions = list(self.get_questions())
        if len(questions) <= count:
            return questions
        return random.sample(questions, count)


class Question(models.Model):
    """
    Model for quiz/test questions
    """
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('fill_blank', 'Fill in the Blank'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='questions')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='questions', null=True, blank=True, help_text="Link to reading passage for comprehension questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')
    order = models.PositiveIntegerField(default=0, help_text="Order within passage or topic")

    # Question content
    image = models.ImageField(upload_to='questions/images/', null=True, blank=True)
    audio_file = models.FileField(upload_to='questions/audio/', null=True, blank=True)

    # Answer and explanation
    correct_answer = models.TextField(help_text="Correct answer or answer key. For text questions, separate multiple acceptable answers with commas (e.g., 'smart, clever, intelligent, wise')")
    explanation = models.TextField(blank=True, help_text="Explanation for the correct answer")

    # Points and timing
    points = models.PositiveIntegerField(default=1)
    time_limit = models.PositiveIntegerField(default=45, help_text="Time limit per question in seconds")
    explanation_display_time = models.PositiveIntegerField(default=5, help_text="Time to show explanation in seconds")

    # Settings
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'questions'
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ['topic', 'difficulty', 'created_at']

    def __str__(self):
        return f"{self.topic.title} - {self.question_text[:50]}..."

    def validate_text_answer(self, user_answer):
        """
        Enhanced validation for text-based answers with intelligent matching.
        Returns a tuple: (is_correct, match_type, matched_answer)
        """
        if not user_answer or not user_answer.strip():
            return False, 'empty', None

        # Clean and normalize user answer
        user_answer = self._normalize_answer(user_answer)

        # Handle True/False questions specially
        if self.question_type == 'true_false':
            return self._validate_true_false_answer(user_answer)

        # Get all acceptable answers and normalize them
        acceptable_answers = [self._normalize_answer(answer) for answer in self.correct_answer.split(',')]

        # 1. Exact match (after normalization)
        for answer in acceptable_answers:
            if user_answer == answer:
                return True, 'exact', answer

        # 2. Fuzzy matching for typos (using simple edit distance)
        for answer in acceptable_answers:
            if self._is_similar(user_answer, answer):
                return True, 'similar', answer

        # 3. Partial match (user answer contains or is contained in correct answer)
        for answer in acceptable_answers:
            if len(user_answer) >= 3 and len(answer) >= 3:
                if user_answer in answer or answer in user_answer:
                    return True, 'partial', answer

        # 4. Word-based matching (for multi-word answers)
        user_words = set(user_answer.split())
        for answer in acceptable_answers:
            answer_words = set(answer.split())
            if len(user_words) > 1 and len(answer_words) > 1:
                # If most words match, consider it correct
                common_words = user_words.intersection(answer_words)
                if len(common_words) >= min(len(user_words), len(answer_words)) * 0.7:
                    return True, 'word_match', answer

        # 5. Numeric answer handling
        if self._is_numeric_answer(user_answer, acceptable_answers):
            return True, 'numeric', user_answer

        return False, 'incorrect', None

    def _normalize_answer(self, answer):
        """
        Normalize answer text for better comparison.
        Handles capitalization, extra spaces, and common variations.
        """
        if not answer:
            return ""

        # Convert to lowercase and strip whitespace
        normalized = answer.strip().lower()

        # Remove extra spaces between words
        normalized = ' '.join(normalized.split())

        # Remove common punctuation that doesn't affect meaning
        import re
        normalized = re.sub(r'[.,!?;:]$', '', normalized)

        # Handle common variations
        replacements = {
            'colour': 'color',
            'grey': 'gray',
            'centre': 'center',
            'metre': 'meter',
            'litre': 'liter',
            'realise': 'realize',
            'organise': 'organize',
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        return normalized

    def _validate_true_false_answer(self, user_answer):
        """
        Validate True/False answers with multiple acceptable formats.
        """
        # Normalize the correct answer
        correct_answer = self._normalize_answer(self.correct_answer)

        # Define true/false variations
        true_variations = ['true', 't', 'yes', 'y', '1', 'correct', 'right']
        false_variations = ['false', 'f', 'no', 'n', '0', 'incorrect', 'wrong']

        user_is_true = user_answer in true_variations
        user_is_false = user_answer in false_variations

        correct_is_true = correct_answer in true_variations
        correct_is_false = correct_answer in false_variations

        if (user_is_true and correct_is_true) or (user_is_false and correct_is_false):
            return True, 'exact', correct_answer

        return False, 'incorrect', None

    def _is_numeric_answer(self, user_answer, acceptable_answers):
        """
        Check if the answer is numeric and matches any acceptable numeric answer.
        """
        try:
            user_num = float(user_answer.replace(',', ''))
            for answer in acceptable_answers:
                try:
                    answer_num = float(answer.replace(',', ''))
                    # Allow small floating point differences
                    if abs(user_num - answer_num) < 0.001:
                        return True
                except ValueError:
                    continue
        except ValueError:
            pass

        return False

    def _is_similar(self, word1, word2, threshold=0.8):
        """
        Check if two words are similar using simple edit distance.
        Returns True if similarity is above threshold.
        """
        if abs(len(word1) - len(word2)) > 2:
            return False

        # Simple Levenshtein distance calculation
        def levenshtein_distance(s1, s2):
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        distance = levenshtein_distance(word1, word2)
        max_len = max(len(word1), len(word2))
        similarity = 1 - (distance / max_len)

        return similarity >= threshold

    def get_acceptable_answers_list(self):
        """Return list of all acceptable answers for display."""
        return [answer.strip() for answer in self.correct_answer.split(',')]

    def get_choices(self):
        """Get all answer choices for multiple choice questions"""
        return self.answer_choices.all().order_by('order')

    def get_correct_choice(self):
        """Get the correct answer choice for multiple choice questions"""
        return self.answer_choices.filter(is_correct=True).first()


class AnswerChoice(models.Model):
    """
    Model for multiple choice answer options
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'answer_choices'
        verbose_name = 'Answer Choice'
        verbose_name_plural = 'Answer Choices'
        ordering = ['question', 'order']

    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.choice_text}"


class Quiz(models.Model):
    """
    Model for quizzes (practice sessions for topics)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='quizzes')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='quizzes')

    # Quiz settings
    total_questions = models.PositiveIntegerField(default=10)
    time_limit = models.PositiveIntegerField(default=300, help_text="Time limit in seconds")

    # Shuffling and randomization
    question_ids = models.JSONField(default=list, help_text="Shuffled question IDs for this quiz attempt")
    seed = models.IntegerField(default=0, help_text="Random seed for consistent shuffling")

    # Status
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Results
    score = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    time_taken = models.PositiveIntegerField(default=0, help_text="Time taken in seconds")

    # Attempt tracking
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'quizzes'
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.full_name} - {self.topic.title} Quiz (Attempt {self.attempt_number})"

    def calculate_score(self):
        """Calculate quiz score based on answers"""
        correct_answers = self.quiz_answers.filter(is_correct=True).count()
        total_answers = self.quiz_answers.count()

        if total_answers > 0:
            self.percentage = (correct_answers / total_answers) * 100
            self.score = correct_answers
            self.total_points = total_answers
        else:
            self.percentage = 0
            self.score = 0
            self.total_points = 0

        self.save()
        return self.percentage


class QuizAnswer(models.Model):
    """
    Model for storing user answers to quiz questions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    time_taken = models.PositiveIntegerField(default=0, help_text="Time taken in seconds")

    # Metadata
    answered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'quiz_answers'
        verbose_name = 'Quiz Answer'
        verbose_name_plural = 'Quiz Answers'
        unique_together = ['quiz', 'question']

    def __str__(self):
        return f"{self.quiz.user.full_name} - {self.question.question_text[:30]}..."


class Test(models.Model):
    """
    Model for topic tests (more formal assessment than quizzes)
    """
    TEST_TYPES = [
        ('topic_test', 'Topic Test'),
        ('level_exam', 'Level Exam'),
        ('practice_test', 'Practice Test'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey('subjects.Topic', on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    class_level = models.ForeignKey('subjects.ClassLevel', on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tests')

    # Test settings
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default='topic_test')
    total_questions = models.PositiveIntegerField(default=10)
    time_limit = models.PositiveIntegerField(default=1800, help_text="Time limit in seconds")
    pass_percentage = models.PositiveIntegerField(default=60)

    # Question shuffling and randomization
    question_ids = models.JSONField(default=list, help_text="Shuffled question IDs for this exam attempt")
    seed = models.IntegerField(default=0, help_text="Random seed for consistent shuffling")

    # Status
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    # Results
    score = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    passed = models.BooleanField(default=False)

    # Attempts
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'tests'
        verbose_name = 'Test'
        verbose_name_plural = 'Tests'
        ordering = ['-started_at']

    def __str__(self):
        if self.topic:
            return f"{self.user.full_name} - {self.topic.title} Test"
        elif self.class_level:
            return f"{self.user.full_name} - {self.class_level.name} Exam"
        return f"{self.user.full_name} - Test"

    def calculate_score(self):
        """Calculate test score based on answers"""
        correct_answers = self.test_answers.filter(is_correct=True).count()
        total_answers = self.test_answers.count()

        if total_answers > 0:
            self.percentage = (correct_answers / total_answers) * 100
            self.score = correct_answers
            self.total_points = total_answers
            self.passed = self.percentage >= self.pass_percentage
        else:
            self.percentage = 0
            self.score = 0
            self.total_points = 0
            self.passed = False

        self.save()
        return self.percentage


class TestAnswer(models.Model):
    """
    Model for storing user answers to test questions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.PositiveIntegerField(default=0)
    time_taken = models.PositiveIntegerField(default=0, help_text="Time taken in seconds")

    # Metadata
    answered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'test_answers'
        verbose_name = 'Test Answer'
        verbose_name_plural = 'Test Answers'
        unique_together = ['test', 'question']

    def __str__(self):
        return f"{self.test.user.full_name} - {self.question.question_text[:30]}..."






