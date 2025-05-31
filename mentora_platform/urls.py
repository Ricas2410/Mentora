"""
URL configuration for mentora_platform project.

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

    # API endpoints
    path('api/user/current-progress/', UserCurrentProgressAPIView.as_view(), name='api_user_current_progress'),
    path('api/user/grade-<int:grade_number>/subjects/', UserGradeSubjectsAPIView.as_view(), name='api_user_grade_subjects'),
    path('api/user/stats/', UserStatsAPIView.as_view(), name='api_user_stats'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
