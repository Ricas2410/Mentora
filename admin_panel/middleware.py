"""
Middleware for admin panel functionality
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.conf import settings as django_settings
from .models import SiteSettings


class MaintenanceModeMiddleware:
    """
    Middleware to handle maintenance mode functionality.
    When maintenance mode is enabled, only logged-in staff users can access the site.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if maintenance mode is enabled
        try:
            site_settings = SiteSettings.get_settings()
            maintenance_mode = site_settings.maintenance_mode
            maintenance_message = site_settings.maintenance_message
        except:
            # If settings can't be loaded, assume maintenance mode is off
            maintenance_mode = False
            maintenance_message = "The site is currently under maintenance. Please check back later."

        # If maintenance mode is enabled
        if maintenance_mode:
            # Allow access to admin panel and static files
            if (request.path.startswith('/my-admin/') or 
                request.path.startswith('/static/') or 
                request.path.startswith('/media/') or
                request.path.startswith('/admin/')):
                return self.get_response(request)
            
            # Allow access for staff users (admins)
            if request.user.is_authenticated and request.user.is_staff:
                return self.get_response(request)
            
            # Block all other users with maintenance page
            return self.render_maintenance_page(request, maintenance_message)

        # Normal operation - process request
        return self.get_response(request)

    def render_maintenance_page(self, request, message):
        """
        Render the maintenance mode page for blocked users
        """
        maintenance_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Site Under Maintenance - Mentora Learning Platform</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .maintenance-container {{
                    background: white;
                    border-radius: 20px;
                    padding: 3rem;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 600px;
                    margin: 2rem;
                }}
                .maintenance-icon {{
                    font-size: 4rem;
                    color: #667eea;
                    margin-bottom: 1.5rem;
                    animation: pulse 2s infinite;
                }}
                @keyframes pulse {{
                    0% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                    100% {{ transform: scale(1); }}
                }}
                .maintenance-title {{
                    color: #2d3748;
                    font-weight: 700;
                    margin-bottom: 1rem;
                }}
                .maintenance-message {{
                    color: #4a5568;
                    font-size: 1.1rem;
                    line-height: 1.6;
                    margin-bottom: 2rem;
                }}
                .admin-login-btn {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    padding: 0.75rem 2rem;
                    border-radius: 50px;
                    color: white;
                    text-decoration: none;
                    font-weight: 600;
                    transition: transform 0.2s;
                }}
                .admin-login-btn:hover {{
                    transform: translateY(-2px);
                    color: white;
                    text-decoration: none;
                }}
                .estimated-time {{
                    background: #f7fafc;
                    border-radius: 10px;
                    padding: 1rem;
                    margin: 1.5rem 0;
                    border-left: 4px solid #667eea;
                }}
                @media (max-width: 768px) {{
                    .maintenance-container {{
                        padding: 2rem 1.5rem;
                        margin: 1rem;
                    }}
                    .maintenance-icon {{
                        font-size: 3rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="maintenance-container">
                <div class="maintenance-icon">
                    <i class="fas fa-tools"></i>
                </div>
                
                <h1 class="maintenance-title">We'll Be Right Back!</h1>
                
                <div class="maintenance-message">
                    {message}
                </div>
                
                <div class="estimated-time">
                    <i class="fas fa-clock me-2"></i>
                    <strong>We're working hard to improve your learning experience.</strong><br>
                    <small class="text-muted">Thank you for your patience!</small>
                </div>
                
                <div class="mt-4">
                    <a href="/my-admin/" class="admin-login-btn">
                        <i class="fas fa-user-shield me-2"></i>
                        Admin Access
                    </a>
                </div>
                
                <div class="mt-4">
                    <small class="text-muted">
                        <i class="fas fa-graduation-cap me-1"></i>
                        Mentora Learning Platform
                    </small>
                </div>
            </div>
            
            <script>
                // Auto-refresh every 30 seconds to check if maintenance is over
                setTimeout(function() {{
                    window.location.reload();
                }}, 30000);
            </script>
        </body>
        </html>
        """
        
        return HttpResponse(maintenance_html, status=503)
