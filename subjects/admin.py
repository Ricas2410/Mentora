from django.contrib import admin
from .models import Subject, ClassLevel, Topic


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('order', 'name')


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'level_number', 'pass_percentage', 'is_active')
    list_filter = ('subject', 'is_active', 'created_at')
    search_fields = ('name', 'subject__name', 'description')
    ordering = ('subject', 'level_number')

    fieldsets = (
        (None, {'fields': ('subject', 'name', 'level_number', 'description')}),
        ('Prerequisites', {'fields': ('prerequisite_level',)}),
        ('Settings', {'fields': ('is_active', 'pass_percentage')}),
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_level', 'order', 'difficulty_level', 'estimated_duration', 'is_active')
    list_filter = ('class_level__subject', 'class_level', 'difficulty_level', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'class_level__name')
    ordering = ('class_level', 'order')

    fieldsets = (
        (None, {'fields': ('class_level', 'title', 'description')}),
        ('Organization', {'fields': ('order', 'estimated_duration', 'difficulty_level')}),
        ('Settings', {'fields': ('is_active',)}),
    )
