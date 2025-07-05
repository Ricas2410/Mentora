from django.contrib import admin
from .models import SystemSettings, Notification, CSVImportLog, HeroSection, SiteStatistic, UserFeedback


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'description', 'cta_text')
        }),
        ('Media', {
            'fields': ('hero_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SiteStatistic)
class SiteStatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'icon', 'order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'value']
    list_editable = ['order', 'is_active']
    ordering = ['order']


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    search_fields = ['key', 'value', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'user__email', 'title', 'message']
    readonly_fields = ['created_at', 'read_at']


@admin.register(CSVImportLog)
class CSVImportLogAdmin(admin.ModelAdmin):
    list_display = ['import_type', 'file_name', 'status', 'total_rows', 'successful_rows', 'started_at']
    list_filter = ['import_type', 'status', 'started_at']
    search_fields = ['file_name', 'imported_by__username']
    readonly_fields = ['started_at', 'completed_at', 'success_rate']


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'feedback_type', 'rating', 'star_rating', 'is_resolved', 'created_at']
    list_filter = ['feedback_type', 'rating', 'is_resolved', 'created_at']
    search_fields = ['user__email', 'user__username', 'message', 'page_url']
    readonly_fields = ['created_at', 'updated_at', 'user_agent', 'ip_address']
    list_editable = ['is_resolved']
    ordering = ['-created_at']

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'ip_address', 'user_agent')
        }),
        ('Feedback Details', {
            'fields': ('rating', 'feedback_type', 'message', 'include_screenshot', 'page_url')
        }),
        ('Admin', {
            'fields': ('is_resolved', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_display(self, obj):
        return obj.user.email if obj.user else 'Anonymous'
    user_display.short_description = 'User'
    user_display.admin_order_field = 'user__email'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
