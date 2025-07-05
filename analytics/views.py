from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
import os
from django.db import connection
from django.contrib.auth import get_user_model
from .models import PageVisit, SystemMetrics, UserActivity, ErrorLog

# Optional import for system monitoring
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

User = get_user_model()


@method_decorator(staff_member_required, name='dispatch')
class AnalyticsDashboardView(TemplateView):
    template_name = 'analytics/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Time ranges
        now = timezone.now()
        last_24h = now - timedelta(hours=24)
        last_7d = now - timedelta(days=7)
        last_30d = now - timedelta(days=30)

        # System metrics
        context['system_metrics'] = self.get_system_metrics()

        # User statistics
        context['user_stats'] = self.get_user_statistics(last_24h, last_7d, last_30d)

        # Page visit statistics
        context['visit_stats'] = self.get_visit_statistics(last_24h, last_7d, last_30d)

        # Error statistics
        context['error_stats'] = self.get_error_statistics(last_24h, last_7d)

        # Geographic data
        context['geographic_data'] = self.get_geographic_data(last_7d)

        # Recent activity
        context['recent_activities'] = UserActivity.objects.select_related('user')[:10]
        context['recent_errors'] = ErrorLog.objects.filter(resolved=False)[:5]

        return context

    def get_system_metrics(self):
        """Get current system metrics"""
        if not PSUTIL_AVAILABLE:
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'memory_total': 0,
                'memory_used': 0,
                'disk_usage': 0,
                'disk_total': 0,
                'disk_used': 0,
                'db_size': 'N/A',
                'psutil_available': False,
            }

        try:
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Database size (PostgreSQL specific)
            db_size = None
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
                    db_size = cursor.fetchone()[0]
            except:
                pass

            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_total': memory.total,
                'memory_used': memory.used,
                'disk_usage': disk.percent,
                'disk_total': disk.total,
                'disk_used': disk.used,
                'db_size': db_size,
                'psutil_available': True,
            }
        except Exception as e:
            return {
                'cpu_usage': 0,
                'memory_usage': 0,
                'memory_total': 0,
                'memory_used': 0,
                'disk_usage': 0,
                'disk_total': 0,
                'disk_used': 0,
                'db_size': 'Unknown',
                'error': str(e)
            }

    def get_user_statistics(self, last_24h, last_7d, last_30d):
        """Get user statistics"""
        total_users = User.objects.count()
        new_users_24h = User.objects.filter(date_joined__gte=last_24h).count()
        new_users_7d = User.objects.filter(date_joined__gte=last_7d).count()
        new_users_30d = User.objects.filter(date_joined__gte=last_30d).count()

        # Active users (users who visited in the last 24h)
        active_users_24h = PageVisit.objects.filter(
            timestamp__gte=last_24h,
            user__isnull=False
        ).values('user').distinct().count()

        return {
            'total_users': total_users,
            'new_users_24h': new_users_24h,
            'new_users_7d': new_users_7d,
            'new_users_30d': new_users_30d,
            'active_users_24h': active_users_24h,
        }

    def get_visit_statistics(self, last_24h, last_7d, last_30d):
        """Get page visit statistics"""
        visits_24h = PageVisit.objects.filter(timestamp__gte=last_24h).count()
        visits_7d = PageVisit.objects.filter(timestamp__gte=last_7d).count()
        visits_30d = PageVisit.objects.filter(timestamp__gte=last_30d).count()

        # Popular pages
        popular_pages = PageVisit.objects.filter(
            timestamp__gte=last_7d
        ).values('page_url', 'page_title').annotate(
            visit_count=Count('id')
        ).order_by('-visit_count')[:10]

        # Device breakdown
        device_breakdown = PageVisit.objects.filter(
            timestamp__gte=last_7d
        ).values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'visits_24h': visits_24h,
            'visits_7d': visits_7d,
            'visits_30d': visits_30d,
            'popular_pages': popular_pages,
            'device_breakdown': device_breakdown,
        }

    def get_error_statistics(self, last_24h, last_7d):
        """Get error statistics"""
        errors_24h = ErrorLog.objects.filter(timestamp__gte=last_24h).count()
        errors_7d = ErrorLog.objects.filter(timestamp__gte=last_7d).count()
        unresolved_errors = ErrorLog.objects.filter(resolved=False).count()

        # Error types
        error_types = ErrorLog.objects.filter(
            timestamp__gte=last_7d
        ).values('error_type').annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        return {
            'errors_24h': errors_24h,
            'errors_7d': errors_7d,
            'unresolved_errors': unresolved_errors,
            'error_types': error_types,
        }

    def get_geographic_data(self, last_7d):
        """Get geographic distribution of visitors"""
        return PageVisit.objects.filter(
            timestamp__gte=last_7d,
            country__isnull=False
        ).exclude(country='').values('country').annotate(
            count=Count('id')
        ).order_by('-count')[:10]
