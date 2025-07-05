"""
Analytics utilities for Pentora platform
Advanced analytics, A/B testing, and business intelligence functions
"""

import json
import random
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Count, Avg, Q, F
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import (
    PageVisit, UserActivity, ConversionFunnel, ABTestVariant, 
    ABTestAssignment, UserEngagementMetrics, SystemPerformanceMetrics
)

User = get_user_model()


class AnalyticsManager:
    """Centralized analytics management"""
    
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour
    
    def track_page_visit(self, request, page_title=""):
        """Track a page visit with enhanced data"""
        try:
            # Get or create page visit
            visit_data = {
                'user': request.user if request.user.is_authenticated else None,
                'session_key': request.session.session_key,
                'ip_address': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'page_url': request.build_absolute_uri(),
                'page_title': page_title,
                'referrer': request.META.get('HTTP_REFERER', ''),
                'device_type': self.detect_device_type(request),
            }
            
            # Add geographic data if available
            geo_data = self.get_geographic_data(visit_data['ip_address'])
            visit_data.update(geo_data)
            
            PageVisit.objects.create(**visit_data)
            
            # Track conversion funnel
            self.track_conversion_stage(request, 'visitor')
            
        except Exception as e:
            # Log error but don't break the request
            import logging
            logger = logging.getLogger('Pentora')
            logger.error(f"Analytics tracking error: {e}")
    
    def track_user_activity(self, user, activity_type, metadata=None):
        """Track user activity with metadata"""
        try:
            UserActivity.objects.create(
                user=user,
                activity_type=activity_type,
                metadata=metadata or {},
                ip_address=getattr(user, '_current_ip', None)
            )
            
            # Update engagement metrics
            self.update_engagement_metrics(user)
            
        except Exception as e:
            import logging
            logger = logging.getLogger('Pentora')
            logger.error(f"Activity tracking error: {e}")
    
    def track_conversion_stage(self, request, stage):
        """Track user through conversion funnel"""
        try:
            ConversionFunnel.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                stage=stage,
                metadata={
                    'page_url': request.build_absolute_uri(),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                }
            )
        except Exception as e:
            pass  # Silent fail for conversion tracking
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def detect_device_type(self, request):
        """Detect device type from user agent"""
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            return 'mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'tablet'
        elif 'bot' in user_agent or 'crawler' in user_agent or 'spider' in user_agent:
            return 'bot'
        else:
            return 'desktop'
    
    def get_geographic_data(self, ip_address):
        """Get geographic data for IP address (placeholder)"""
        # In production, integrate with a service like MaxMind GeoIP
        return {
            'country': '',
            'city': '',
            'region': '',
        }
    
    def update_engagement_metrics(self, user):
        """Update daily engagement metrics for user"""
        try:
            today = timezone.now().date()
            
            metrics, created = UserEngagementMetrics.objects.get_or_create(
                user=user,
                date=today,
                defaults={
                    'session_count': 1,
                    'pages_viewed': 1,
                }
            )
            
            if not created:
                metrics.session_count = F('session_count') + 1
                metrics.pages_viewed = F('pages_viewed') + 1
                metrics.save(update_fields=['session_count', 'pages_viewed'])
                
        except Exception as e:
            pass  # Silent fail for engagement tracking


class ABTestManager:
    """A/B testing management"""
    
    def get_variant_for_user(self, user_or_session, test_name):
        """Get A/B test variant for user or session"""
        cache_key = f"ab_test_{test_name}_{user_or_session}"
        variant = cache.get(cache_key)
        
        if variant:
            return variant
        
        # Get active variants for test
        variants = ABTestVariant.objects.filter(
            test_name=test_name,
            is_active=True
        )
        
        if not variants.exists():
            return None
        
        # Check existing assignment
        if isinstance(user_or_session, User):
            assignment = ABTestAssignment.objects.filter(
                user=user_or_session,
                variant__test_name=test_name
            ).first()
        else:
            assignment = ABTestAssignment.objects.filter(
                session_key=user_or_session,
                variant__test_name=test_name
            ).first()
        
        if assignment:
            variant = assignment.variant
        else:
            # Assign new variant based on traffic percentage
            variant = self.assign_variant(variants, user_or_session)
        
        # Cache the result
        cache.set(cache_key, variant, 3600)
        return variant
    
    def assign_variant(self, variants, user_or_session):
        """Assign a variant based on traffic percentages"""
        total_percentage = sum(v.traffic_percentage for v in variants)
        
        if total_percentage == 0:
            return variants.first()
        
        # Generate random number based on user/session for consistency
        if isinstance(user_or_session, User):
            seed = hash(str(user_or_session.id))
        else:
            seed = hash(user_or_session)
        
        random.seed(seed)
        rand_num = random.randint(1, 100)
        
        cumulative = 0
        for variant in variants:
            cumulative += variant.traffic_percentage
            if rand_num <= cumulative:
                # Create assignment record
                assignment_data = {
                    'variant': variant,
                }
                
                if isinstance(user_or_session, User):
                    assignment_data['user'] = user_or_session
                else:
                    assignment_data['session_key'] = user_or_session
                
                ABTestAssignment.objects.create(**assignment_data)
                return variant
        
        return variants.first()


class BusinessIntelligence:
    """Business intelligence and reporting"""
    
    def get_dashboard_metrics(self, days=30):
        """Get key metrics for admin dashboard"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        cache_key = f"dashboard_metrics_{days}_{start_date.date()}"
        metrics = cache.get(cache_key)
        
        if metrics:
            return metrics
        
        # User metrics
        total_users = User.objects.filter(is_active=True, is_staff=False).count()
        new_users = User.objects.filter(
            created_at__gte=start_date,
            is_active=True,
            is_staff=False
        ).count()
        
        # Activity metrics
        page_views = PageVisit.objects.filter(timestamp__gte=start_date).count()
        unique_visitors = PageVisit.objects.filter(
            timestamp__gte=start_date
        ).values('ip_address').distinct().count()
        
        # Engagement metrics
        avg_session_duration = UserEngagementMetrics.objects.filter(
            date__gte=start_date.date()
        ).aggregate(avg_duration=Avg('avg_session_duration'))['avg_duration'] or 0
        
        # Conversion funnel
        funnel_data = self.get_conversion_funnel_data(start_date, end_date)
        
        # Popular content
        popular_pages = PageVisit.objects.filter(
            timestamp__gte=start_date
        ).values('page_url').annotate(
            visits=Count('id')
        ).order_by('-visits')[:10]
        
        metrics = {
            'total_users': total_users,
            'new_users': new_users,
            'page_views': page_views,
            'unique_visitors': unique_visitors,
            'avg_session_duration': avg_session_duration,
            'funnel_data': funnel_data,
            'popular_pages': list(popular_pages),
            'user_growth_rate': self.calculate_growth_rate('users', days),
            'engagement_rate': self.calculate_engagement_rate(start_date, end_date),
        }
        
        # Cache for 1 hour
        cache.set(cache_key, metrics, 3600)
        return metrics
    
    def get_conversion_funnel_data(self, start_date, end_date):
        """Get conversion funnel data"""
        stages = ['visitor', 'signup', 'first_quiz', 'first_lesson', 'active_learner']
        
        funnel_data = []
        for stage in stages:
            count = ConversionFunnel.objects.filter(
                stage=stage,
                timestamp__gte=start_date,
                timestamp__lte=end_date
            ).values('user', 'session_key').distinct().count()
            
            funnel_data.append({
                'stage': stage,
                'count': count
            })
        
        return funnel_data
    
    def calculate_growth_rate(self, metric_type, days):
        """Calculate growth rate for a metric"""
        end_date = timezone.now()
        current_period_start = end_date - timedelta(days=days)
        previous_period_start = current_period_start - timedelta(days=days)
        
        if metric_type == 'users':
            current_count = User.objects.filter(
                created_at__gte=current_period_start,
                is_active=True,
                is_staff=False
            ).count()
            
            previous_count = User.objects.filter(
                created_at__gte=previous_period_start,
                created_at__lt=current_period_start,
                is_active=True,
                is_staff=False
            ).count()
        else:
            return 0
        
        if previous_count == 0:
            return 100 if current_count > 0 else 0
        
        return ((current_count - previous_count) / previous_count) * 100
    
    def calculate_engagement_rate(self, start_date, end_date):
        """Calculate user engagement rate"""
        total_users = User.objects.filter(
            is_active=True,
            is_staff=False,
            created_at__lt=end_date
        ).count()
        
        if total_users == 0:
            return 0
        
        engaged_users = UserActivity.objects.filter(
            timestamp__gte=start_date,
            timestamp__lte=end_date
        ).values('user').distinct().count()
        
        return (engaged_users / total_users) * 100
    
    def get_user_retention_data(self, cohort_days=30):
        """Get user retention data by cohort"""
        # This would implement cohort analysis
        # For now, return placeholder data
        return {
            'day_1': 85,
            'day_7': 65,
            'day_30': 45,
            'day_90': 30,
        }


# Global instances
analytics_manager = AnalyticsManager()
ab_test_manager = ABTestManager()
business_intelligence = BusinessIntelligence()
