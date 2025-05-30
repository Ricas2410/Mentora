# Generated manually to handle slug field addition with data migration

from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    """Populate slug fields for existing records"""
    Subject = apps.get_model('subjects', 'Subject')
    Topic = apps.get_model('subjects', 'Topic')
    
    # Handle Subject slugs
    for subject in Subject.objects.all():
        base_slug = slugify(subject.name)
        slug = base_slug
        counter = 1
        
        # Ensure unique slug
        while Subject.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        subject.slug = slug
        subject.save()
    
    # Handle Topic slugs
    for topic in Topic.objects.all():
        base_slug = slugify(topic.title)
        slug = base_slug
        counter = 1
        
        # Ensure unique slug within the same class level
        while Topic.objects.filter(slug=slug, class_level=topic.class_level).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        topic.slug = slug
        topic.save()


def reverse_populate_slugs(apps, schema_editor):
    """Reverse migration - clear slug fields"""
    Subject = apps.get_model('subjects', 'Subject')
    Topic = apps.get_model('subjects', 'Topic')
    
    Subject.objects.update(slug='')
    Topic.objects.update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0001_initial'),
    ]

    operations = [
        # Add slug field to Subject (nullable first)
        migrations.AddField(
            model_name='subject',
            name='slug',
            field=models.SlugField(max_length=120, blank=True, null=True),
        ),
        # Add slug field to Topic (nullable first)
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.SlugField(max_length=220, blank=True, null=True),
        ),
        # Populate the slug fields
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
        # Make slug fields non-nullable and unique
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='slug',
            field=models.SlugField(max_length=220),
        ),
    ]
