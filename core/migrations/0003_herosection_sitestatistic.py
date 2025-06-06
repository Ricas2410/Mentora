# Generated by Django 5.2.1 on 2025-05-27 20:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='An Easy Way to Learn and Grow', max_length=200)),
                ('subtitle', models.CharField(default='No matter your background', max_length=200)),
                ('description', models.TextField(default='Quality education for everyone. Start your learning journey today with our comprehensive, mobile-friendly platform designed specifically for Ghanaian learners.')),
                ('hero_image', models.ImageField(blank=True, help_text='Upload a high-quality image for the hero section (recommended: 1920x1080px)', null=True, upload_to='hero_images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])])),
                ('cta_text', models.CharField(default='Get Started Free', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Hero Section',
                'verbose_name_plural': 'Hero Sections',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SiteStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=50)),
                ('icon', models.CharField(default='fas fa-chart-line', help_text="FontAwesome icon class (e.g., 'fas fa-users')", max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Site Statistic',
                'verbose_name_plural': 'Site Statistics',
                'ordering': ['order'],
            },
        ),
    ]
