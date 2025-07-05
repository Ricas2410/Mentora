#!/usr/bin/env python3
"""
Script to check Supabase configuration for media file uploads
"""
import os
from decouple import config

def check_supabase_config():
    """Check if Supabase configuration is properly set up"""
    print("🔍 Checking Supabase Configuration...")
    print("=" * 50)
    
    # Check required environment variables
    required_vars = [
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY', 
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_S3_ENDPOINT_URL',
        'AWS_S3_CUSTOM_DOMAIN'
    ]
    
    missing_vars = []
    configured_vars = {}
    
    for var in required_vars:
        value = config(var, default='')
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'SECRET' in var:
                masked_value = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '***'
                configured_vars[var] = masked_value
            else:
                configured_vars[var] = value
        else:
            missing_vars.append(var)
    
    print("✅ Configured Variables:")
    for var, value in configured_vars.items():
        print(f"   {var}: {value}")
    
    if missing_vars:
        print("\n❌ Missing Variables:")
        for var in missing_vars:
            print(f"   {var}")
        
        print("\n📋 To fix this, set these environment variables:")
        print("   fly secrets set AWS_ACCESS_KEY_ID=your_access_key")
        print("   fly secrets set AWS_SECRET_ACCESS_KEY=your_secret_key")
        print("   fly secrets set AWS_STORAGE_BUCKET_NAME=your_bucket_name")
        print("   fly secrets set AWS_S3_ENDPOINT_URL=your_endpoint_url")
        print("   fly secrets set AWS_S3_CUSTOM_DOMAIN=your_custom_domain")
        
        return False
    else:
        print("\n✅ All required Supabase variables are configured!")
        return True

def test_supabase_connection():
    """Test if Supabase endpoint is reachable"""
    print("\n🔗 Testing Supabase Connection...")
    
    try:
        import requests
        endpoint = config('AWS_S3_ENDPOINT_URL', default='')
        if not endpoint:
            print("❌ No endpoint URL configured")
            return False
        
        # Test the endpoint
        test_url = endpoint.replace('/storage/v1/s3', '')
        print(f"Testing: {test_url}")
        
        response = requests.head(test_url, timeout=10)
        if response.status_code == 200:
            print("✅ Supabase endpoint is reachable")
            return True
        else:
            print(f"❌ Endpoint returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Pentora Platform - Supabase Configuration Checker")
    print("=" * 60)
    
    config_ok = check_supabase_config()
    
    if config_ok:
        connection_ok = test_supabase_connection()
        
        if connection_ok:
            print("\n🎉 Supabase is properly configured and reachable!")
            print("Media files should upload to Supabase storage.")
        else:
            print("\n⚠️  Supabase is configured but not reachable.")
            print("Check your endpoint URL and network connectivity.")
    else:
        print("\n❌ Supabase is not properly configured.")
        print("Media files will fall back to local storage.")
    
    print("\n📋 Next steps:")
    print("1. Set missing environment variables if any")
    print("2. Deploy the application: python deploy_fixes.py")
    print("3. Test media file uploads after deployment") 