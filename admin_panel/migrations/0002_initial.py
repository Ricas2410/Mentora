# Generated by Django 5.2.1 on 2025-07-05 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='adminactivity',
            name='admin_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_activities', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_updates', to=settings.AUTH_USER_MODEL),
        ),
    ]
