from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import json


class VisitorAccessMiddleware:
    """
    Middleware to handle visitor access to learning content.
    Allows visitors to browse subjects and quizzes but prompts for login when trying to access content.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that visitors can access without login
        self.public_urls = [
            '/',
            '/login/',
            '/register/',
            '/subjects/',
            '/about/',
            '/contact/',
            '/help/',
            '/privacy/',
            '/terms/',
        ]
        
        # URL patterns that visitors can browse but need login to access content
        self.browse_only_patterns = [
            '/subjects/',  # Can browse subjects
            '/quiz/',      # Can see quiz list but not take quizzes
        ]
        
        # URL patterns that require login to access
        self.login_required_patterns = [
            '/dashboard/',
            '/progress/',
            '/profile/',
            '/study/',
            '/take/',
            '/result/',
            '/exam/',
        ]

    def __call__(self, request):
        # Skip middleware for authenticated users
        if request.user.is_authenticated:
            return self.get_response(request)
            
        # Skip middleware for public URLs
        if self.is_public_url(request.path):
            return self.get_response(request)
            
        # Handle browse-only patterns
        if self.is_browse_only_url(request.path):
            # Allow GET requests for browsing
            if request.method == 'GET':
                return self.get_response(request)
            else:
                return self.redirect_to_login(request, "Please sign in to continue")
                
        # Handle login required patterns
        if self.is_login_required_url(request.path):
            return self.redirect_to_login(request, "Please sign in or create an account to access this content")
            
        # Default: allow access
        return self.get_response(request)
    
    def is_public_url(self, path):
        """Check if URL is completely public"""
        for url in self.public_urls:
            if path.startswith(url):
                return True
        return False
    
    def is_browse_only_url(self, path):
        """Check if URL allows browsing but requires login for actions"""
        for pattern in self.browse_only_patterns:
            if path.startswith(pattern):
                return True
        return False
    
    def is_login_required_url(self, path):
        """Check if URL requires login"""
        for pattern in self.login_required_patterns:
            if pattern in path:
                return True
        return False
    
    def redirect_to_login(self, request, message):
        """Redirect to login with appropriate message"""
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'Authentication required',
                'message': message,
                'login_url': reverse('users:login')
            }, status=401)
        
        # Add message for regular requests
        messages.info(request, message)
        
        # Redirect to login with next parameter
        login_url = reverse('users:login')
        if request.path != '/':
            login_url += f'?next={request.path}'
        
        return redirect(login_url)


class LoginPromptMiddleware:
    """
    Middleware to add login prompts to content that visitors can see but not access.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add login prompt context for unauthenticated users on certain pages
        if not request.user.is_authenticated and hasattr(request, 'resolver_match'):
            if request.resolver_match and request.resolver_match.app_name in ['subjects', 'content']:
                # Add a flag to indicate login prompt should be shown
                if hasattr(response, 'context_data'):
                    response.context_data['show_login_prompt'] = True
                    response.context_data['login_message'] = "Sign in to start learning and track your progress!"
        
        return response


class WWWRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to handle WWW redirects for SEO
    """

    def process_request(self, request):
        """
        Redirect www to non-www or vice versa based on settings
        """
        if not hasattr(settings, 'PREPEND_WWW'):
            return None

        host = request.get_host().lower()

        # Skip for localhost and development
        if 'localhost' in host or '127.0.0.1' in host:
            return None

        # Handle WWW redirect
        if settings.PREPEND_WWW:
            # Redirect non-www to www
            if not host.startswith('www.'):
                new_host = f"www.{host}"
                new_url = f"{request.scheme}://{new_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)
        else:
            # Redirect www to non-www (default)
            if host.startswith('www.'):
                new_host = host[4:]  # Remove 'www.'
                new_url = f"{request.scheme}://{new_host}{request.get_full_path()}"
                return HttpResponsePermanentRedirect(new_url)

        return None


class IPCanonicalizationMiddleware(MiddlewareMixin):
    """
    Middleware to redirect IP addresses to domain name for SEO
    """

    def process_request(self, request):
        """
        Redirect IP address access to proper domain
        """
        host = request.get_host().lower()

        # Skip for localhost and development
        if 'localhost' in host or '127.0.0.1' in host:
            return None

        # Check if accessing via IP address
        import re
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}(:\d+)?$'

        if re.match(ip_pattern, host):
            # Get proper domain from settings
            proper_domain = getattr(settings, 'SITE_DOMAIN', 'mentora.pythonanywhere.com')
            protocol = getattr(settings, 'SITE_PROTOCOL', 'https')

            # Redirect to proper domain
            new_url = f"{protocol}://{proper_domain}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)

        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security and performance headers
    """

    def process_response(self, request, response):
        """
        Add security and caching headers
        """
        # Security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Cache headers for static content
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            # Cache static files for 1 year
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
            response['Expires'] = 'Thu, 31 Dec 2025 23:59:59 GMT'
        elif request.path in ['/sitemap.xml', '/robots.txt']:
            # Cache sitemap and robots.txt for 1 day
            response['Cache-Control'] = 'public, max-age=86400'
        else:
            # Don't cache dynamic content
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

        return response



