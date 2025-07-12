from django.urls import path
from . import views
from . import feedback_views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('about-pentora-ghana/', views.AboutPentoraGhanaView.as_view(), name='about_pentora_ghana'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('help/', views.HelpView.as_view(), name='help'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),

    # Feedback
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),

    # Feedback Management (Admin)
    path('feedback-management/', feedback_views.FeedbackListView.as_view(), name='feedback_list'),
    path('feedback-management/<uuid:feedback_id>/', feedback_views.FeedbackDetailView.as_view(), name='feedback_detail'),
    path('feedback-management/<uuid:feedback_id>/update/', feedback_views.update_feedback_status, name='update_feedback_status'),
    path('feedback-management/bulk-action/', feedback_views.bulk_feedback_action, name='bulk_feedback_action'),
    path('feedback-management/analytics/', feedback_views.feedback_analytics, name='feedback_analytics'),

    # SEO URLs
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_txt_view, name='robots'),

    # Test URLs
    path('test-static/', views.test_static_files, name='test_static'),
]
