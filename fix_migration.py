#!/usr/bin/env python3
"""
Fix migration issue with admin_activities foreign key
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pentora_platform.settings')
django.setup()

def check_users_and_fix_migration():
    """Check existing users and fix migration issue"""
    print("🔍 Checking Users and Migration Issue...")
    print("=" * 50)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Check existing users
    users = User.objects.all()
    print(f"📊 Total users in database: {users.count()}")
    
    if users.exists():
        print("\n👥 Existing users:")
        for user in users:
            print(f"   ID: {user.id}, Username: {user.username}, Email: {user.email}, Is Staff: {user.is_staff}")
    else:
        print("❌ No users found in database")
    
    # Check if there are any admin activities
    try:
        from admin_panel.models import AdminActivity
        activities = AdminActivity.objects.all()
        print(f"\n📋 Admin activities: {activities.count()}")
        
        if activities.exists():
            print("Current admin activities:")
            for activity in activities:
                print(f"   ID: {activity.id}, Action: {activity.action}, Admin User ID: {getattr(activity, 'admin_user_id', 'Not set')}")
    except Exception as e:
        print(f"⚠️  Could not check admin activities: {e}")
    
    # Check if the problematic migration has been applied
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='admin_activities'
        """)
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            cursor.execute("PRAGMA table_info(admin_activities)")
            columns = cursor.fetchall()
            print(f"\n📋 Admin activities table columns:")
            for col in columns:
                print(f"   {col[1]} ({col[2]})")
    
    print("\n" + "=" * 50)
    print("📋 Recommended Solutions:")
    
    if users.exists():
        first_user = users.first()
        print(f"1. Use existing user ID {first_user.id} for the migration")
        print(f"2. Create a superuser if needed")
    else:
        print("1. Create a superuser first")
        print("2. Then run the migration")
    
    print("3. Or modify the migration to handle the foreign key properly")

def create_fixed_migration():
    """Create a fixed migration file"""
    print("\n🔧 Creating Fixed Migration...")
    print("=" * 50)
    
    # Create a new migration file that handles the foreign key properly
    migration_content = '''# Generated manually to fix foreign key issue

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def set_admin_user_for_existing_activities(apps, schema_editor):
    """Set admin_user for existing activities"""
    User = apps.get_model('users', 'User')
    AdminActivity = apps.get_model('admin_panel', 'AdminActivity')
    
    # Get the first user (or create one if needed)
    if User.objects.exists():
        first_user = User.objects.first()
        
        # Update existing activities
        AdminActivity.objects.filter(admin_user__isnull=True).update(admin_user=first_user)
    else:
        # If no users exist, we'll need to handle this differently
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_remove_sitesettings_dashboard_banner_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # First add the field as nullable
        migrations.AddField(
            model_name='adminactivity',
            name='admin_user',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_activities', to=settings.AUTH_USER_MODEL),
        ),
        
        # Run the data migration
        migrations.RunPython(set_admin_user_for_existing_activities),
        
        # Then make it non-nullable
        migrations.AlterField(
            model_name='adminactivity',
            name='admin_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_activities', to=settings.AUTH_USER_MODEL),
        ),
        
        # Add the sitesettings field
        migrations.AddField(
            model_name='sitesettings',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings_updates', to=settings.AUTH_USER_MODEL),
        ),
    ]
'''
    
    # Write the fixed migration
    migration_path = 'admin_panel/migrations/0005_adminactivity_admin_user_sitesettings_updated_by_fixed.py'
    with open(migration_path, 'w') as f:
        f.write(migration_content)
    
    print(f"✅ Created fixed migration: {migration_path}")
    print("\n📋 Next steps:")
    print("1. Delete the problematic migration file")
    print("2. Rename the fixed migration to replace it")
    print("3. Run migrations again")

def main():
    """Main function"""
    print("🚀 Migration Fix Script")
    print("=" * 60)
    
    check_users_and_fix_migration()
    create_fixed_migration()

if __name__ == "__main__":
    main() 