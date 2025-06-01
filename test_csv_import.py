#!/usr/bin/env python
"""
Test script for CSV import functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentora_platform.settings')
django.setup()

from core.utils.csv_import import CSVImporter
from users.models import User

def test_csv_import():
    """Test the CSV import functionality"""
    print("🧪 Testing CSV Import Functionality...")
    
    # Get admin user
    admin_user = User.objects.filter(is_staff=True).first()
    if not admin_user:
        print("❌ No admin user found!")
        return False
    
    print(f"✅ Using admin user: {admin_user.email}")
    
    # Test with the CSV file
    try:
        with open('test_questions_import.csv', 'r', encoding='utf-8') as f:
            csv_content = f.read()
        
        print(f"📄 CSV file loaded: {len(csv_content)} characters")
        
        # Import the CSV
        importer = CSVImporter('questions', csv_content, admin_user)
        result = importer.import_data()
        
        print("\n📊 Import Results:")
        print(f"  ✅ Success: {result.get('success')}")
        print(f"  📝 Total rows: {result.get('total_rows')}")
        print(f"  ✅ Successful: {result.get('successful_rows')}")
        print(f"  ❌ Failed: {result.get('failed_rows')}")
        
        if result.get('errors'):
            print(f"\n⚠️ Errors ({len(result['errors'])}):")
            for i, error in enumerate(result['errors'][:5]):
                print(f"    {i+1}. {error}")
            if len(result['errors']) > 5:
                print(f"    ... and {len(result['errors']) - 5} more errors")
        
        if result.get('success') and result.get('successful_rows', 0) > 0:
            print("\n🎉 CSV import test PASSED!")
            return True
        else:
            print("\n❌ CSV import test FAILED!")
            return False
            
    except Exception as e:
        print(f"❌ Error during CSV import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_csv_import()
