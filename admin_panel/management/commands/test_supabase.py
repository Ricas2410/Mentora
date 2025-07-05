"""
Management command to test Supabase storage connectivity
"""
from django.core.management.base import BaseCommand
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class Command(BaseCommand):
    help = 'Test Supabase storage connectivity and list buckets'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Testing Supabase connectivity...")
        
        try:
            # Create S3 client with Supabase credentials
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            self.stdout.write(f"🔑 Access Key: {settings.AWS_ACCESS_KEY_ID[:8]}...")
            self.stdout.write(f"🔗 Endpoint: {settings.AWS_S3_ENDPOINT_URL}")
            
            # Test connection by listing buckets
            self.stdout.write("📋 Listing buckets...")
            response = s3_client.list_buckets()
            
            self.stdout.write("✅ Successfully connected to Supabase!")
            self.stdout.write("📦 Available buckets:")
            for bucket in response['Buckets']:
                self.stdout.write(f"  - {bucket['Name']}")
                
            # Test if our bucket exists
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            try:
                s3_client.head_bucket(Bucket=bucket_name)
                self.stdout.write(f"✅ Bucket '{bucket_name}' exists and is accessible")
                
                # List objects in bucket
                self.stdout.write(f"📁 Objects in '{bucket_name}':")
                objects = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=10)
                if 'Contents' in objects:
                    for obj in objects['Contents']:
                        self.stdout.write(f"  - {obj['Key']} ({obj['Size']} bytes)")
                else:
                    self.stdout.write("  (bucket is empty)")
                    
            except ClientError as e:
                if e.response['Error']['Code'] == '404':
                    self.stdout.write(f"❌ Bucket '{bucket_name}' does not exist")
                else:
                    self.stdout.write(f"❌ Error accessing bucket: {e}")
                    
        except Exception as e:
            self.stdout.write(f"❌ Connection failed: {str(e)}")
            self.stdout.write("💡 Check your Supabase credentials and endpoint URL")
            
        self.stdout.write("\n✅ Supabase test completed!")
