from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
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
