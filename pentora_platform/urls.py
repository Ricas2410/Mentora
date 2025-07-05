"""
URL configuration for pentora_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import sitemaps
from core.views import robots_txt_view, health_check, track_performance, offline_view
from django.views.generic import RedirectView
from subjects.views import UserCurrentProgressAPIView, UserGradeSubjectsAPIView
from users.views import UserStatsAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my-admin/', include('admin_panel.urls')),
    path('', include('core.urls')),
    path('auth/', include('users.urls')),
    path('subjects/', include('subjects.urls')),
    path('content/', include('content.urls')),
    path('progress/', include('progress.urls')),
    path('billing/', include('billing.urls')),
    path('analytics/', include('analytics.urls')),

    # SEO and utility endpoints
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt_view, name='robots_txt'),
    path('offline/', offline_view, name='offline'),
    path('health/', health_check, name='health_check'),

    # API endpoints
    path('api/user/current-progress/', UserCurrentProgressAPIView.as_view(), name='api_user_current_progress'),
    path('api/user/grade-<int:grade_number>/subjects/', UserGradeSubjectsAPIView.as_view(), name='api_user_grade_subjects'),
    path('api/user/stats/', UserStatsAPIView.as_view(), name='api_user_stats'),
    path('api/analytics/performance/', track_performance, name='track_performance'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
