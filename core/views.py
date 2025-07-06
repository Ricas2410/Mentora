from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from subjects.models import Subject, ClassLevel, Topic
from progress.models import UserProgress
from .models import HeroSection, SiteStatistic, UserFeedback
from .seo import SEOManager, MetaTagsHelper
import logging

logger = logging.getLogger('Pentora')


class HomeView(TemplateView):
    """
    Home page view
    """
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # SEO optimization
        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="Pentora - Free Online Learning Platform for Grades 1-12 | Quality Education for All",
            description="Access comprehensive educational content, interactive quizzes, and study materials for all grades. Learn English, Mathematics, Science, Social Studies, ICT, and Life Skills - completely free!",
            keywords="free online learning, educational platform, grades 1-12, online quizzes, study materials, English, Mathematics, Science, free education, online school, learning platform"
        ))

        # Structured data for organization
        context['structured_data'] = seo_manager.generate_structured_data('organization', {})

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

        # Additional homepage statistics
        context.update({
            'total_subjects': Subject.objects.filter(is_active=True).count(),
            'total_topics': Topic.objects.filter(is_active=True).count(),
            'recent_topics': Topic.objects.filter(is_active=True).order_by('-created_at')[:8],
        })

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
        """Handle level selection with improved error handling"""
        import logging
        logger = logging.getLogger(__name__)

        logger.info(f"Dashboard POST request from user {request.user.id}")
        logger.info(f"POST data: {request.POST}")

        if 'class_level' in request.POST:
            try:
                class_level_str = request.POST['class_level']
                logger.info(f"Received class_level: '{class_level_str}'")

                if not class_level_str:
                    logger.warning("Empty class_level received")
                    messages.error(request, 'No class level selected. Please select a class level.')
                    return self.get(request, *args, **kwargs)

                class_level = int(class_level_str)
                logger.info(f"Parsed class_level as integer: {class_level}")

                valid_levels = [choice[0] for choice in request.user.CLASS_LEVEL_CHOICES]
                logger.info(f"Valid levels for user: {valid_levels}")

                if class_level in valid_levels:
                    # Update user's class level
                    old_level = request.user.current_class_level
                    request.user.current_class_level = class_level
                    request.user.save(update_fields=['current_class_level', 'updated_at'])

                    logger.info(f"Successfully updated user {request.user.id} class level from {old_level} to {class_level}")

                    # Add success message
                    messages.success(request, f'Class level updated to Grade {class_level}!')

                    return redirect('core:dashboard')
                else:
                    logger.warning(f"Invalid class level {class_level} not in valid levels {valid_levels}")
                    messages.error(request, f'Invalid class level {class_level} selected. Valid options are: {", ".join(map(str, valid_levels))}')

            except (ValueError, TypeError) as e:
                logger.error(f"ValueError/TypeError parsing class_level '{request.POST.get('class_level')}': {str(e)}")
                messages.error(request, f'Invalid class level format: {request.POST.get("class_level")}. Please select a valid option.')
            except Exception as e:
                # Log the error for debugging
                logger.error(f"Dashboard level selection error for user {request.user.id}: {str(e)}", exc_info=True)
                messages.error(request, f'An error occurred while updating your class level: {str(e)}. Please try again.')
        else:
            logger.warning("No class_level in POST data")
            messages.error(request, 'No class level data received. Please try again.')

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
    Generate XML sitemap for SEO with improved structure and priorities
    """
    try:
        from django.template.loader import render_to_string
        from django.conf import settings

        # Get domain from request for better compatibility
        domain = f"{request.scheme}://{request.get_host()}"

        # Get all active content with safe queries
        try:
            subjects = Subject.objects.filter(is_active=True)
        except:
            subjects = []

        try:
            class_levels = ClassLevel.objects.filter(is_active=True)
        except:
            class_levels = []

        try:
            topics = Topic.objects.filter(is_active=True)
        except:
            topics = []

        # Calculate priorities and change frequencies
        high_priority_urls = [
            {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
            {'url': '/subjects/', 'priority': '0.9', 'changefreq': 'weekly'},
            {'url': '/subjects/quiz/', 'priority': '0.9', 'changefreq': 'weekly'},
            {'url': '/subjects/learn/', 'priority': '0.9', 'changefreq': 'weekly'},
        ]

        medium_priority_urls = [
            {'url': '/about/', 'priority': '0.8', 'changefreq': 'monthly'},
            {'url': '/contact/', 'priority': '0.7', 'changefreq': 'monthly'},
            {'url': '/help/', 'priority': '0.6', 'changefreq': 'monthly'},
            {'url': '/auth/register/', 'priority': '0.8', 'changefreq': 'monthly'},
            {'url': '/auth/login/', 'priority': '0.7', 'changefreq': 'monthly'},
        ]

        context = {
            'domain': domain,
            'current_date': timezone.now(),
            'subjects': subjects,
            'class_levels': class_levels,
            'topics': topics,
            'high_priority_urls': high_priority_urls,
            'medium_priority_urls': medium_priority_urls,
        }

        xml_content = render_to_string('sitemap.xml', context, request=request)
        return HttpResponse(xml_content, content_type='application/xml')

    except Exception as e:
        # Fallback simple sitemap if there are any errors
        domain = f"{request.scheme}://{request.get_host()}"
        simple_sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{domain}/</loc>
        <lastmod>{timezone.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{domain}/subjects/</loc>
        <lastmod>{timezone.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{domain}/about/</loc>
        <lastmod>{timezone.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{domain}/contact/</loc>
        <lastmod>{timezone.now().strftime('%Y-%m-%d')}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>'''
        return HttpResponse(simple_sitemap, content_type='application/xml')


def robots_txt_view(request):
    """
    Generate robots.txt for SEO
    """
    domain = f"{request.scheme}://{request.get_host()}"

    robots_content = f"""User-agent: *
Allow: /

# Sitemap
Sitemap: {domain}/sitemap.xml

# Disallow admin and private areas
Disallow: /admin/
Disallow: /my-admin/
Disallow: /auth/logout/
Disallow: /auth/password/
Disallow: /api/private/
Disallow: /media/private/
Disallow: /users/profile/
Disallow: /users/dashboard/
Disallow: /analytics/
Disallow: /billing/

# Encourage crawling of educational content for better search visibility
# This helps with searches for: education, online learning, e-learning, Mentora, Pentora
# BECE preparation, WASSCE preparation, Ghana education, online studies
Allow: /
Allow: /subjects/
Allow: /subjects/learn/
Allow: /subjects/quiz/
Allow: /content/
Allow: /content/study-notes/
Allow: /content/exam/
Allow: /about/
Allow: /contact/
Allow: /help/
Allow: /auth/register/
Allow: /auth/login/

# Crawl delay for respectful crawling
Crawl-delay: 1

# Cache directive for better performance
Cache-delay: 86400
"""

    return HttpResponse(robots_content, content_type='text/plain')


def custom_404_view(request, exception):
    """
    Custom 404 error page with SEO-friendly content and navigation
    """
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """
    Custom 500 error page for server errors
    """
    logger.error(f"500 error on {request.path}")
    return render(request, '500.html', status=500)


@require_http_methods(["GET"])
def offline_view(request):
    """Offline page for PWA"""
    return render(request, 'core/offline.html', {
        'title': 'You\'re Offline - Pentora',
        'description': 'You\'re currently offline. Some features may be limited.'
    })


@require_http_methods(["POST"])
@csrf_exempt
def track_performance(request):
    """Track performance metrics from frontend - CSRF exempt for analytics"""
    try:
        import json
        data = json.loads(request.body)

        # Only log significant performance data to avoid spam
        load_time = data.get('loadTime', 0)
        if load_time > 100:  # Only log if load time > 100ms
            logger.info(f"Performance: Load time {load_time}ms, "
                       f"DOM ready {data.get('domContentLoaded', 0)}ms, "
                       f"URL: {data.get('url', 'unknown')}")

        return JsonResponse({'status': 'success'})
    except Exception as e:
        logger.error(f"Performance tracking error: {e}")
        return JsonResponse({'status': 'error'}, status=400)


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Basic database check
        Subject.objects.first()

        return JsonResponse({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=503)


class AboutView(TemplateView):
    """About page with SEO optimization"""
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="About Pentora - Empowering Education for All | Our Mission & Vision",
            description="Learn about Pentora's mission to provide free, quality education to underprivileged learners worldwide. Discover our story, values, and commitment to educational equity.",
            keywords="about Pentora, educational mission, free education, underprivileged learners, educational equity, online learning platform"
        ))

        return context


class ContactView(TemplateView):
    """Contact page"""
    template_name = 'core/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="Contact Pentora - Get Help & Support | Educational Platform",
            description="Need help with Pentora? Contact our support team for assistance with learning, technical issues, or general inquiries. We're here to help!",
            keywords="contact Pentora, support, help, customer service, educational support"
        ))

        return context


class HelpView(TemplateView):
    """Help center"""
    template_name = 'core/help.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="Help Center - Pentora Learning Platform | FAQs & Guides",
            description="Find answers to common questions about using Pentora. Browse our comprehensive help guides, tutorials, and FAQs to get the most out of your learning experience.",
            keywords="Pentora help, FAQ, learning guides, tutorials, how to use Pentora, educational platform help"
        ))

        return context


def test_static_files(request):
    """Test view to check if static files are being served correctly"""
    from django.conf import settings
    import os
    
    static_root = settings.STATIC_ROOT
    static_url = settings.STATIC_URL
    
    # Check if static files exist
    test_files = [
        'css/enhanced-ui.css',
        'js/app.js',
        'js/progress-bar-cleanup.js',
        'js/ux-enhancements.js',
        'js/mobile-navigation.js',
        'js/performance-optimizer.js',
        'js/ui-interactions.js',
        'js/page-specific-enhancements.js',
        'sw.js',
        'manifest.json'
    ]
    
    file_status = {}
    for file_path in test_files:
        full_path = os.path.join(static_root, file_path)
        exists = os.path.exists(full_path)
        file_status[file_path] = {
            'exists': exists,
            'url': f"{static_url}{file_path}",
            'full_path': full_path
        }
    
    context = {
        'file_status': file_status,
        'static_root': static_root,
        'static_url': static_url,
        'debug': settings.DEBUG,
        'staticfiles_storage': settings.STATICFILES_STORAGE,
    }
    
    return render(request, 'core/test_static.html', context)


class PrivacyView(TemplateView):
    """
    Privacy Policy page view
    """
    template_name = 'core/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # SEO optimization
        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="Privacy Policy - Pentora Educational Platform",
            description="Learn how Pentora protects your privacy and personal information. Our comprehensive privacy policy explains data collection, usage, and security practices.",
            keywords="privacy policy, data protection, personal information, privacy rights, data security, educational platform privacy"
        ))

        return context


class TermsView(TemplateView):
    """
    Terms of Service page view
    """
    template_name = 'core/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # SEO optimization
        seo_manager = SEOManager(self.request)
        context.update(seo_manager.get_meta_tags(
            title="Terms of Service - Pentora Educational Platform",
            description="Read our terms of service to understand your rights and responsibilities when using Pentora educational platform.",
            keywords="terms of service, user agreement, terms and conditions, educational platform terms, user rights, service terms"
        ))

        return context


@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):
    """
    Handle feedback form submission via AJAX
    """
    try:
        import json

        # Parse JSON data
        data = json.loads(request.body)

        # Get client IP
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip

        # Create feedback record
        feedback = UserFeedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            rating=data.get('rating'),
            feedback_type=data.get('feedback_type', 'general'),
            message=data.get('message', ''),
            include_screenshot=data.get('include_screenshot', False),
            page_url=request.META.get('HTTP_REFERER', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            ip_address=get_client_ip(request)
        )

        logger.info(f"Feedback submitted: {feedback.id} by {feedback.user or 'Anonymous'}")

        return JsonResponse({
            'success': True,
            'message': 'Thank you for your feedback! We appreciate your input.'
        })

    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Sorry, there was an error submitting your feedback. Please try again.'
        }, status=500)
