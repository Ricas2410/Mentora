# Generated migration for optimizing question queries

from django.db import migrations, models


def create_indexes_if_tables_exist(apps, schema_editor):
    """Create indexes only if tables exist"""
    db_alias = schema_editor.connection.alias

    # SQLite-compatible index creation
    with schema_editor.connection.cursor() as cursor:
        # Check if tables exist and create indexes
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='content_question';")
            if cursor.fetchone():
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_active_topic ON content_question(is_active, topic_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_type_difficulty ON content_question(question_type, difficulty);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_created_at ON content_question(created_at);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_topic_active_type ON content_question(topic_id, is_active, question_type);")
                print("✅ Created question indexes")
        except Exception as e:
            print(f"⚠️ Could not create question indexes: {e}")

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subjects_topic';")
            if cursor.fetchone():
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_topic_class_level ON subjects_topic(class_level_id);")
                print("✅ Created topic indexes")
        except Exception as e:
            print(f"⚠️ Could not create topic indexes: {e}")

        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subjects_classlevel';")
            if cursor.fetchone():
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_class_level_subject ON subjects_classlevel(subject_id, level_number);")
                print("✅ Created class level indexes")
        except Exception as e:
            print(f"⚠️ Could not create class level indexes: {e}")


def remove_indexes(apps, schema_editor):
    """Remove indexes"""
    with schema_editor.connection.cursor() as cursor:
        try:
            cursor.execute("DROP INDEX IF EXISTS idx_question_active_topic;")
            cursor.execute("DROP INDEX IF EXISTS idx_question_type_difficulty;")
            cursor.execute("DROP INDEX IF EXISTS idx_question_created_at;")
            cursor.execute("DROP INDEX IF EXISTS idx_question_topic_active_type;")
            cursor.execute("DROP INDEX IF EXISTS idx_topic_class_level;")
            cursor.execute("DROP INDEX IF EXISTS idx_class_level_subject;")
        except Exception as e:
            print(f"⚠️ Could not remove indexes: {e}")


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_indexes_if_tables_exist, remove_indexes),
    ]
