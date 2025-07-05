import re
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import PageVisit, UserActivity
from django.contrib.auth import get_user_model

User = get_user_model()


class AnalyticsMiddleware(MiddlewareMixin):
    """Middleware to track page visits and user activity"""
    
    # URLs to exclude from tracking
    EXCLUDE_PATHS = [
        r'^/admin/',
        r'^/static/',
        r'^/media/',
        r'^/favicon\.ico$',
        r'^/robots\.txt$',
        r'^/sitemap\.xml$',
        r'^/api/',
        r'^/analytics/dashboard/',  # Don't track analytics dashboard visits
    ]
    
    # Bot user agents to exclude
    BOT_USER_AGENTS = [
        'bot', 'crawler', 'spider', 'scraper', 'facebook', 'twitter',
        'linkedin', 'whatsapp', 'telegram', 'googlebot', 'bingbot',
        'slurp', 'duckduckbot', 'baiduspider', 'yandexbot'
    ]
    
    def process_request(self, request):
        """Track page visits"""
        
        # Skip if path should be excluded
        if self.should_exclude_path(request.path):
            return None
        
        # Skip if it's a bot
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if any(bot in user_agent for bot in self.BOT_USER_AGENTS):
            return None
        
        # Skip if it's not a GET request
        if request.method != 'GET':
            return None
        
        try:
            # Get client information
            ip_address = self.get_client_ip(request)
            user_agent_full = request.META.get('HTTP_USER_AGENT', '')
            referrer = request.META.get('HTTP_REFERER', '')
            
            # Determine device type
            device_type = self.get_device_type(user_agent_full)
            
            # Get page information
            page_url = request.build_absolute_uri()
            page_title = self.extract_page_title(request)
            
            # Create page visit record
            PageVisit.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                ip_address=ip_address,
                user_agent=user_agent_full,
                page_url=page_url,
                page_title=page_title,
                referrer=referrer if referrer else None,
                device_type=device_type,
                # Geographic data would be populated by a separate service
                country='',
                city='',
                region='',
            )
            
            # Track user activity for authenticated users
            if request.user.is_authenticated:
                # Determine activity type based on URL
                activity_type = self.get_activity_type(request.path)
                if activity_type:
                    UserActivity.objects.create(
                        user=request.user,
                        activity_type=activity_type,
                        description=f"Visited {page_title or request.path}",
                        metadata={
                            'url': request.path,
                            'method': request.method,
                            'user_agent': user_agent_full[:200],  # Truncate for storage
                        },
                        ip_address=ip_address,
                    )
        
        except Exception as e:
            # Don't break the request if analytics fails
            print(f"Analytics middleware error: {e}")
        
        return None
    
    def should_exclude_path(self, path):
        """Check if path should be excluded from tracking"""
        for pattern in self.EXCLUDE_PATHS:
            if re.match(pattern, path):
                return True
        return False
    
    def get_client_ip(self, request):
        """Get the real client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def get_device_type(self, user_agent):
        """Determine device type from user agent"""
        user_agent = user_agent.lower()
        
        if any(bot in user_agent for bot in self.BOT_USER_AGENTS):
            return 'bot'
        elif any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipod']):
            return 'mobile'
        elif any(tablet in user_agent for tablet in ['tablet', 'ipad']):
            return 'tablet'
        else:
            return 'desktop'
    
    def extract_page_title(self, request):
        """Extract page title from URL path"""
        path = request.path.strip('/')
        
        # Map common paths to titles
        title_map = {
            '': 'Home',
            'auth/login': 'Login',
            'auth/register': 'Register',
            'auth/profile': 'Profile',
            'subjects': 'Subjects',
            'billing/plans': 'Subscription Plans',
            'billing/dashboard': 'Billing Dashboard',
            'my-admin': 'Admin Dashboard',
        }
        
        # Check exact matches first
        if path in title_map:
            return title_map[path]
        
        # Check partial matches
        for key, title in title_map.items():
            if key and path.startswith(key):
                return title
        
        # Generate title from path
        if path:
            return path.replace('/', ' > ').replace('-', ' ').replace('_', ' ').title()
        
        return 'Unknown Page'
    
    def get_activity_type(self, path):
        """Determine activity type from URL path"""
        if '/auth/login' in path:
            return 'login'
        elif '/auth/logout' in path:
            return 'logout'
        elif '/auth/profile' in path:
            return 'profile_update'
        elif '/subjects/' in path and '/quiz/' in path:
            return 'quiz_start'
        elif '/subjects/' in path and '/lesson/' in path:
            return 'lesson_view'
        elif '/billing/' in path:
            return 'subscription_change'
        
        return None  # Don't track generic page views as activities
