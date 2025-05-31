from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),

    # API endpoints
    path('api/stats/', views.UserStatsAPIView.as_view(), name='api_user_stats'),
    path('verify-email/<str:token>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('resend-verification/', views.ResendVerificationView.as_view(), name='resend_verification'),

    # Password Reset URLs
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-sent/', views.PasswordResetSentView.as_view(), name='password_reset_sent'),
    path('password-reset-confirm/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
