"""
Sitemap generation for Pentora platform
Comprehensive SEO sitemap including all public content
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from subjects.models import Subject, ClassLevel, Topic
from content.models import StudyNote
from datetime import datetime, timedelta


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages - Enhanced for education search visibility"""
    priority = 0.9
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'core:help',
            'core:privacy',
            'core:terms',
            'subjects:list',
            'subjects:simple_learn',
            'subjects:quiz_list',
            'users:register',
            'users:login',
        ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()

    def priority(self, item):
        priorities = {
            'core:home': 1.0,
            'subjects:list': 0.9,
            'subjects:simple_learn': 0.9,
            'subjects:quiz_list': 0.8,
            'users:register': 0.7,
            'users:login': 0.6,
            'core:about': 0.6,
            'core:contact': 0.5,
            'core:help': 0.7,
            'core:privacy': 0.4,
            'core:terms': 0.4,
        }
        return priorities.get(item, 0.5)

    def changefreq(self, item):
        frequencies = {
            'core:home': 'daily',
            'subjects:list': 'weekly',
            'subjects:simple_learn': 'weekly',
            'subjects:quiz_list': 'weekly',
            'users:register': 'monthly',
            'users:login': 'monthly',
            'core:about': 'monthly',
            'core:contact': 'monthly',
            'core:help': 'monthly',
            'core:privacy': 'yearly',
            'core:terms': 'yearly',
        }
        return frequencies.get(item, 'weekly')


class SubjectSitemap(Sitemap):
    """Sitemap for subjects"""
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Subject.objects.filter(is_active=True).order_by('order', 'name')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('subjects:detail', args=[obj.slug])

    def priority(self, obj):
        # Higher priority for subjects with more content
        topic_count = Topic.objects.filter(
            class_level__subject=obj,
            is_active=True
        ).count()
        
        if topic_count > 50:
            return 0.9
        elif topic_count > 20:
            return 0.8
        else:
            return 0.7


class ClassLevelSitemap(Sitemap):
    """Sitemap for class levels"""
    changefreq = 'weekly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return ClassLevel.objects.filter(
            is_active=True,
            subject__is_active=True
        ).select_related('subject').order_by('subject__order', 'level_number')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('subjects:class_detail', args=[obj.subject.slug, obj.level_number])

    def priority(self, obj):
        # Higher priority for levels with more topics
        topic_count = obj.topics.filter(is_active=True).count()
        
        if topic_count > 20:
            return 0.8
        elif topic_count > 10:
            return 0.7
        else:
            return 0.6


class TopicSitemap(Sitemap):
    """Sitemap for topics"""
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'
    limit = 5000  # Limit to prevent huge sitemaps

    def items(self):
        return Topic.objects.filter(
            is_active=True,
            class_level__is_active=True,
            class_level__subject__is_active=True
        ).select_related(
            'class_level__subject'
        ).order_by(
            'class_level__subject__order',
            'class_level__level_number',
            'order'
        )[:self.limit]

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('subjects:topic_detail', args=[
            obj.class_level.subject.slug,
            obj.class_level.level_number,
            obj.slug
        ])

    def priority(self, obj):
        # Higher priority for topics with study notes and questions
        has_notes = obj.study_notes.filter(is_active=True).exists()
        has_questions = obj.questions.filter(is_active=True).exists()
        
        if has_notes and has_questions:
            return 0.7
        elif has_notes or has_questions:
            return 0.6
        else:
            return 0.5

    def changefreq(self, obj):
        # More frequent updates for recently modified topics
        if obj.updated_at > timezone.now() - timedelta(days=7):
            return 'daily'
        elif obj.updated_at > timezone.now() - timedelta(days=30):
            return 'weekly'
        else:
            return 'monthly'


class StudyNoteSitemap(Sitemap):
    """Sitemap for study notes (if they have individual pages)"""
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'
    limit = 2000

    def items(self):
        return StudyNote.objects.filter(
            is_active=True,
            topic__is_active=True,
            topic__class_level__is_active=True,
            topic__class_level__subject__is_active=True
        ).select_related(
            'topic__class_level__subject'
        ).order_by('-updated_at')[:self.limit]

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Assuming study notes have individual URLs
        return reverse('content:study_note_detail', args=[
            obj.topic.class_level.subject.slug,
            obj.topic.class_level.level_number,
            obj.topic.slug,
            obj.id
        ])

    def priority(self, obj):
        # Higher priority for longer, more comprehensive notes
        content_length = len(obj.content)
        
        if content_length > 2000:
            return 0.6
        elif content_length > 1000:
            return 0.5
        else:
            return 0.4


class QuizSitemap(Sitemap):
    """Sitemap for quiz pages"""
    changefreq = 'weekly'
    priority = 0.6
    protocol = 'https'

    def items(self):
        # Return topics that have quizzes
        return Topic.objects.filter(
            is_active=True,
            class_level__is_active=True,
            class_level__subject__is_active=True,
            questions__is_active=True,
            questions__question_type='quiz'
        ).distinct().select_related(
            'class_level__subject'
        ).order_by(
            'class_level__subject__order',
            'class_level__level_number',
            'order'
        )

    def lastmod(self, obj):
        # Get the latest question update time
        latest_question = obj.questions.filter(
            is_active=True,
            question_type='quiz'
        ).order_by('-updated_at').first()
        
        return latest_question.updated_at if latest_question else obj.updated_at

    def location(self, obj):
        return reverse('subjects:topic_quiz', args=[
            obj.class_level.subject.slug,
            obj.class_level.level_number,
            obj.slug
        ])

    def priority(self, obj):
        # Higher priority for topics with more quiz questions
        question_count = obj.questions.filter(
            is_active=True,
            question_type='quiz'
        ).count()
        
        if question_count > 20:
            return 0.7
        elif question_count > 10:
            return 0.6
        else:
            return 0.5


# Sitemap index
sitemaps = {
    'static': StaticViewSitemap,
    'subjects': SubjectSitemap,
    'class_levels': ClassLevelSitemap,
    'topics': TopicSitemap,
    'study_notes': StudyNoteSitemap,
    'quizzes': QuizSitemap,
}
