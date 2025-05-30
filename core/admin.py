from django.contrib import admin
from .models import SystemSettings, Notification, CSVImportLog, HeroSection, SiteStatistic


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
