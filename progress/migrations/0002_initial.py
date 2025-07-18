# Generated by Django 5.2.1 on 2025-07-05 14:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0002_initial'),
        ('progress', '0001_initial'),
        ('subjects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studynoteprogress',
            name='study_note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='content.studynote'),
        ),
        migrations.AddField(
            model_name='studynoteprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studysession',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_sessions', to='subjects.topic'),
        ),
        migrations.AddField(
            model_name='studysession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_sessions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='topicprogress',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='subjects.topic'),
        ),
        migrations.AddField(
            model_name='topicprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='class_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='subjects.classlevel'),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='achievement',
            unique_together={('user', 'achievement_type')},
        ),
        migrations.AlterUniqueTogether(
            name='studynoteprogress',
            unique_together={('user', 'study_note')},
        ),
        migrations.AlterUniqueTogether(
            name='topicprogress',
            unique_together={('user', 'topic')},
        ),
        migrations.AlterUniqueTogether(
            name='userprogress',
            unique_together={('user', 'class_level')},
        ),
    ]
