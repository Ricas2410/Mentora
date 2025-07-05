from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Public billing pages
    path('', views.BillingPlansView.as_view(), name='index'),
    path('plans/', views.BillingPlansView.as_view(), name='plans'),
    path('announcement/', views.ActivationAnnouncementView.as_view(), name='announcement'),
    
    # User billing management
    path('dashboard/', views.BillingDashboardView.as_view(), name='dashboard'),
    path('subscribe/<uuid:plan_id>/', views.SubscribeView.as_view(), name='subscribe'),
    path('cancel/', views.CancelSubscriptionView.as_view(), name='cancel'),
    path('reactivate/', views.ReactivateSubscriptionView.as_view(), name='reactivate'),
    
    # API endpoints
    path('api/status/', views.billing_status_api, name='api_status'),
    path('api/currency/', views.CurrencyConversionView.as_view(), name='api_currency'),

    # Paystack integration
    path('paystack/pay/', views.PaystackPaymentView.as_view(), name='paystack_pay'),
    path('paystack/callback/', views.PaystackCallbackView.as_view(), name='paystack_callback'),
    path('paystack/webhook/', views.PaystackWebhookView.as_view(), name='paystack_webhook'),

    # Webhooks
    path('webhook/', views.BillingWebhookView.as_view(), name='webhook'),
]
