from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import PageVisit, SystemMetrics, UserActivity, ErrorLog


@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['page_title', 'user_display', 'ip_address', 'country', 'device_type', 'timestamp']
    list_filter = ['device_type', 'country', 'timestamp']
    search_fields = ['page_url', 'page_title', 'user__email', 'ip_address']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

    def user_display(self, obj):
        if obj.user:
            return obj.user.email
        return f"Anonymous ({obj.session_key[:8]}...)"
    user_display.short_description = 'User'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'cpu_usage_display', 'memory_usage_display', 'disk_usage_display', 'active_users', 'page_views_last_hour']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

    def cpu_usage_display(self, obj):
        color = 'red' if obj.cpu_usage > 80 else 'orange' if obj.cpu_usage > 60 else 'green'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, obj.cpu_usage
        )
    cpu_usage_display.short_description = 'CPU Usage'

    def memory_usage_display(self, obj):
        color = 'red' if obj.memory_usage > 80 else 'orange' if obj.memory_usage > 60 else 'green'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, obj.memory_usage
        )
    memory_usage_display.short_description = 'Memory Usage'

    def disk_usage_display(self, obj):
        color = 'red' if obj.disk_usage > 80 else 'orange' if obj.disk_usage > 60 else 'green'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, obj.disk_usage
        )
    disk_usage_display.short_description = 'Disk Usage'


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description_short', 'timestamp']
    list_filter = ['activity_type', 'timestamp']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'description']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['error_type', 'user', 'request_url', 'resolved_display', 'timestamp']
    list_filter = ['error_type', 'resolved', 'timestamp']
    search_fields = ['error_type', 'error_message', 'user__email', 'request_url']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    actions = ['mark_resolved', 'mark_unresolved']

    def resolved_display(self, obj):
        if obj.resolved:
            return format_html('<span style="color: green;">✓ Resolved</span>')
        return format_html('<span style="color: red;">✗ Unresolved</span>')
    resolved_display.short_description = 'Status'

    def mark_resolved(self, request, queryset):
        queryset.update(resolved=True)
        self.message_user(request, f"{queryset.count()} errors marked as resolved.")
    mark_resolved.short_description = "Mark selected errors as resolved"

    def mark_unresolved(self, request, queryset):
        queryset.update(resolved=False)
        self.message_user(request, f"{queryset.count()} errors marked as unresolved.")
    mark_unresolved.short_description = "Mark selected errors as unresolved"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
