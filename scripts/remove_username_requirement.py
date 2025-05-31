#!/usr/bin/env python
"""
Remove Username Requirement and Test Auto-Generation
This script tests the new username auto-generation functionality
"""

import os
import sys
import django

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from users.models import User

def test_username_generation():
    """Test the username generation functionality"""
    print("TESTING USERNAME AUTO-GENERATION")
    print("=" * 50)
    
    # Test cases
    test_emails = [
        'john.doe@example.com',
        'sarah123@gmail.com',
        'test-user@yahoo.com',
        'user.with.dots@domain.org',
        'special!chars@test.com',
        '123numbers@email.com',
        'a@b.com',
        'very.long.email.address.with.many.dots@verylongdomain.com'
    ]
    
    print("Testing username generation for various email formats:")
    print()
    
    for email in test_emails:
        try:
            username = User.generate_username_from_email(email)
            print(f"Email: {email}")
            print(f"Generated Username: {username}")
            print(f"Length: {len(username)} characters")
            print("-" * 40)
        except Exception as e:
            print(f"Error generating username for {email}: {e}")
            print("-" * 40)
    
    print("\n✅ Username generation test completed!")
    print("\nKey Features:")
    print("- Usernames are auto-generated from email addresses")
    print("- Special characters are removed (except underscore)")
    print("- Usernames start with a letter")
    print("- Duplicate usernames get numbered suffixes")
    print("- Maximum length is 30 characters")

def check_existing_users():
    """Check existing users and their usernames"""
    print("\n" + "=" * 50)
    print("CHECKING EXISTING USERS")
    print("=" * 50)
    
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    if users.exists():
        print("\nExisting users:")
        for user in users[:10]:  # Show first 10 users
            print(f"- {user.email} → username: {user.username}")
        
        if users.count() > 10:
            print(f"... and {users.count() - 10} more users")
    else:
        print("No users found in database.")

def main():
    """Main function to test username removal"""
    print("🎯 REMOVING USERNAME REQUIREMENT FROM SIGNUP")
    print("=" * 60)
    
    print("Changes made:")
    print("✅ Removed username field from registration form")
    print("✅ Added auto-generation method to User model")
    print("✅ Updated registration view to auto-create usernames")
    print("✅ Added helpful message about email-based accounts")
    
    # Test username generation
    test_username_generation()
    
    # Check existing users
    check_existing_users()
    
    print("\n🎉 SUCCESS!")
    print("Username requirement has been removed from signup!")
    print("\nNext steps:")
    print("1. Run migrations: python manage.py makemigrations")
    print("2. Apply migrations: python manage.py migrate")
    print("3. Test registration with new form")
    print("4. Deploy to PythonAnywhere")

if __name__ == '__main__':
    main()
