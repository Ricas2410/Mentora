from django.contrib import admin
from .models import StudyNote, Question, AnswerChoice, Quiz, QuizAnswer, Test, TestAnswer


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'order', 'is_active', 'created_at']
    list_filter = ['topic__class_level__subject', 'topic__class_level', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'topic__title']
    ordering = ['topic', 'order']


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4
    fields = ['choice_text', 'is_correct', 'order']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'topic', 'question_type', 'difficulty', 'time_limit', 'explanation_display_time', 'points', 'is_active']
    list_filter = ['topic__class_level__subject', 'topic__class_level', 'question_type', 'difficulty', 'is_active']
    search_fields = ['question_text', 'topic__title']
    inlines = [AnswerChoiceInline]
    fieldsets = (
        ('Question Content', {
            'fields': ('topic', 'question_text', 'question_type', 'difficulty', 'image', 'audio_file')
        }),
        ('Answer & Explanation', {
            'fields': ('correct_answer', 'explanation')
        }),
        ('Timing & Scoring', {
            'fields': ('time_limit', 'explanation_display_time', 'points'),
            'description': 'Configure question timing and scoring settings'
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )

    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'


@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question_short', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__topic__class_level__subject']
    search_fields = ['choice_text', 'question__question_text']

    def question_short(self, obj):
        return obj.question.question_text[:30] + "..." if len(obj.question.question_text) > 30 else obj.question.question_text
    question_short.short_description = 'Question'
