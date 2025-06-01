from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from subjects.models import Subject, ClassLevel, Topic
from progress.models import UserProgress
from .models import HeroSection, SiteStatistic


class HomeView(TemplateView):
    """
    Home page view
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get hero section content
        try:
            hero_section = HeroSection.objects.filter(is_active=True).first()
            context['hero_section'] = hero_section
        except HeroSection.DoesNotExist:
            context['hero_section'] = None

        # Get site statistics
        context['site_statistics'] = SiteStatistic.objects.filter(is_active=True)

        # Get subjects for display
        context['subjects'] = Subject.objects.filter(is_active=True).order_by('order')[:6]  # Limit to 6 for display

        return context




class DashboardView(LoginRequiredMixin, TemplateView):
    """
    User dashboard view
    """
    template_name = 'core/dashboard.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Check if user has set their class level
        if not user.current_class_level:
            context['needs_level_selection'] = True
            context['class_levels'] = user.CLASS_LEVEL_CHOICES
            return context

        # Get user's current progress
        from progress.models import UserProgress, TopicProgress
        from subjects.models import ClassLevel, Subject

        # Get current grade subjects with detailed progress
        from subjects.models import Topic
        from django.urls import reverse

        current_grade_subjects = []
        for subject in Subject.objects.filter(
            classlevels__level_number=user.current_class_level,
            is_active=True
        ).distinct().order_by('order'):
            try:
                class_level = ClassLevel.objects.get(
                    subject=subject,
                    level_number=user.current_class_level
                )

                # Get or create progress for this subject
                progress, created = UserProgress.objects.get_or_create(
                    user=user,
                    class_level=class_level,
                    defaults={'is_started': False}
                )
                if created or progress.total_topics == 0:
                    progress.update_progress()

                # Get topics with progress
                topics = Topic.objects.filter(
                    class_level=class_level,
                    is_active=True
                ).order_by('order')

                # Find next incomplete topic
                next_topic = None
                for topic in topics:
                    try:
                        topic_progress = TopicProgress.objects.get(
                            user=user,
                            topic=topic
                        )
                        if not topic_progress.is_completed:
                            next_topic = topic
                            break
                    except TopicProgress.DoesNotExist:
                        next_topic = topic
                        break

                # Calculate completion stats
                completed_topics = TopicProgress.objects.filter(
                    user=user,
                    topic__class_level=class_level,
                    is_completed=True
                ).count()

                current_grade_subjects.append({
                    'subject': subject,
                    'class_level': class_level,
                    'progress': progress,
                    'topics_count': topics.count(),
                    'completed_topics': completed_topics,
                    'completion_percentage': (completed_topics / topics.count() * 100) if topics.count() > 0 else 0,
                    'next_topic': next_topic,
                    'next_topic_url': reverse('subjects:topic_detail', args=[
                        subject.id, class_level.id, next_topic.id
                    ]) if next_topic else None,
                    'is_completed': progress.is_completed if progress else False
                })
            except ClassLevel.DoesNotExist:
                continue

        # Get recent activity (last 5 topics worked on)
        recent_activity = TopicProgress.objects.filter(
            user=user,
            is_started=True,
            topic__class_level__level_number=user.current_class_level
        ).select_related(
            'topic__class_level__subject'
        ).order_by('-updated_at')[:5]

        # Calculate overall stats for current grade
        total_subjects = len(current_grade_subjects)
        completed_subjects = sum(1 for s in current_grade_subjects if s['is_completed'])
        total_topics = sum(s['topics_count'] for s in current_grade_subjects)
        completed_topics = sum(s['completed_topics'] for s in current_grade_subjects)

        # Get next learning path
        next_learning_path = self.get_next_learning_path(user, current_grade_subjects)

        # Get the class level name
        class_level_name = f'Grade {user.current_class_level}'

        context.update({
            'current_grade_subjects': current_grade_subjects,
            'recent_activity': recent_activity,
            'total_subjects': total_subjects,
            'completed_subjects': completed_subjects,
            'total_topics': total_topics,
            'completed_topics': completed_topics,
            'subjects_completion_rate': (completed_subjects / total_subjects * 100) if total_subjects > 0 else 0,
            'topics_completion_rate': (completed_topics / total_topics * 100) if total_topics > 0 else 0,
            'user_class_level': user.current_class_level,
            'user_class_level_name': class_level_name,
            'next_learning_path': next_learning_path,
        })

        return context

    def get_next_learning_path(self, user, current_grade_subjects):
        """Get the next learning path for the user"""
        from django.urls import reverse

        # Find first incomplete subject
        for subject_data in current_grade_subjects:
            if subject_data['next_topic']:
                return {
                    'type': 'continue_topic',
                    'title': f"Continue: {subject_data['next_topic'].title}",
                    'subject_name': subject_data['subject'].name,
                    'url': subject_data['next_topic_url']
                }

        # All current grade subjects completed
        if user.current_class_level < 12:
            return {
                'type': 'next_grade',
                'title': f"Ready for Grade {user.current_class_level + 1}",
                'subject_name': 'All subjects completed!',
                'url': reverse('core:dashboard')  # Will trigger promotion
            }
        else:
            return {
                'type': 'completed',
                'title': 'Congratulations! All grades completed!',
                'subject_name': 'You\'ve mastered everything!',
                'url': reverse('progress:achievements')
            }

    def post(self, request, *args, **kwargs):
        """Handle level selection"""
        if 'class_level' in request.POST:
            try:
                class_level = int(request.POST['class_level'])
                valid_levels = [choice[0] for choice in request.user.CLASS_LEVEL_CHOICES]
                if class_level in valid_levels:
                    request.user.current_class_level = class_level
                    request.user.save()
                    return redirect('core:dashboard')
            except (ValueError, TypeError):
                pass
        return self.get(request, *args, **kwargs)


class AboutView(TemplateView):
    """
    About page view
    """
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """
    Contact page view
    """
    template_name = 'core/contact.html'


class HelpView(TemplateView):
    """
    Help page view
    """
    template_name = 'core/help.html'


def sitemap_view(request):
    """
    Generate XML sitemap for SEO
    """
    from django.template.loader import render_to_string

    # Get all active subjects, class levels, and topics
    subjects = Subject.objects.filter(is_active=True)
    class_levels = ClassLevel.objects.filter(is_active=True)
    topics = Topic.objects.filter(is_active=True)

    # Get domain
    domain = f"{request.scheme}://{request.get_host()}"

    context = {
        'domain': domain,
        'current_date': timezone.now(),
        'subjects': subjects,
        'class_levels': class_levels,
        'topics': topics,
    }

    xml_content = render_to_string('sitemap.xml', context, request=request)

    return HttpResponse(xml_content, content_type='application/xml')


def robots_txt_view(request):
    """
    Generate robots.txt for SEO
    """
    domain = f"{request.scheme}://{request.get_host()}"

    robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {domain}/sitemap.xml

# Disallow admin areas
Disallow: /admin/
Disallow: /my-admin/
Disallow: /auth/logout/
Disallow: /auth/password/

# Allow important pages
Allow: /
Allow: /learn/
Allow: /quiz/
Allow: /subjects/
Allow: /about/
Allow: /contact/
Allow: /help/
Allow: /auth/register/
Allow: /auth/login/

# Crawl delay
Crawl-delay: 1
"""

    return HttpResponse(robots_content, content_type='text/plain')
