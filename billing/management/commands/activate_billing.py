from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from billing.models import BillingSettings, SubscriptionPlan, UserSubscription
from billing.notifications import send_billing_activation_announcement
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Activate billing system and optionally notify all users'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--send-emails',
            action='store_true',
            help='Send activation announcement emails to all users',
        )
        parser.add_argument(
            '--create-free-plan',
            action='store_true',
            help='Create a free plan for existing users',
        )
        parser.add_argument(
            '--trial-days',
            type=int,
            default=30,
            help='Number of free trial days for new users (default: 30)',
        )
        parser.add_argument(
            '--announcement-title',
            type=str,
            default='Subscription Plans Now Available!',
            help='Title for the billing announcement banner',
        )
        parser.add_argument(
            '--announcement-message',
            type=str,
            default='We\'ve introduced subscription plans to continue providing you with the best learning experience. Check out our flexible plans and start your free trial today!',
            help='Message for the billing announcement banner',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Activating billing system...'))
        
        # Get or create billing settings
        billing_settings = BillingSettings.get_settings()
        
        # Update billing settings
        billing_settings.billing_enabled = True
        billing_settings.free_trial_days = options['trial_days']
        billing_settings.show_billing_announcement = True
        billing_settings.announcement_title = options['announcement_title']
        billing_settings.announcement_message = options['announcement_message']
        billing_settings.announcement_type = 'info'
        billing_settings.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Billing system activated'))
        self.stdout.write(f'   - Free trial days: {options["trial_days"]}')
        self.stdout.write(f'   - Announcement banner: Enabled')
        
        # Create free plan if requested
        if options['create_free_plan']:
            free_plan, created = SubscriptionPlan.objects.get_or_create(
                name='Free',
                defaults={
                    'description': 'Basic access to learning materials',
                    'price': 0,
                    'billing_cycle': 'monthly',
                    'max_subjects': 3,
                    'max_quizzes_per_day': 5,
                    'priority_support': False,
                    'advanced_analytics': False,
                    'offline_access': False,
                    'is_active': True,
                    'sort_order': 0,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('✅ Created free plan'))
                
                # Assign free plan to existing users without subscriptions
                users_without_subscription = User.objects.filter(subscription__isnull=True)
                subscriptions_created = 0
                
                for user in users_without_subscription:
                    UserSubscription.objects.create(
                        user=user,
                        plan=free_plan,
                        status='active',
                        current_period_start=timezone.now(),
                        current_period_end=timezone.now() + timezone.timedelta(days=365),  # 1 year
                    )
                    subscriptions_created += 1
                
                self.stdout.write(self.style.SUCCESS(f'✅ Created {subscriptions_created} free subscriptions for existing users'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Free plan already exists'))
        
        # Send emails if requested
        if options['send_emails']:
            self.stdout.write('📧 Sending activation emails to all users...')
            
            all_users = User.objects.filter(is_active=True, is_email_verified=True)
            total_users = all_users.count()
            
            if total_users == 0:
                self.stdout.write(self.style.WARNING('⚠️  No active verified users found'))
            else:
                sent_count = send_billing_activation_announcement(all_users)
                self.stdout.write(self.style.SUCCESS(f'✅ Sent {sent_count}/{total_users} activation emails'))
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 BILLING ACTIVATION COMPLETE'))
        self.stdout.write('='*50)
        self.stdout.write(f'📊 Total users: {User.objects.count()}')
        self.stdout.write(f'📊 Active subscriptions: {UserSubscription.objects.filter(status="active").count()}')
        self.stdout.write(f'📊 Available plans: {SubscriptionPlan.objects.filter(is_active=True).count()}')
        self.stdout.write('\n🔧 Next steps:')
        self.stdout.write('   1. Configure payment providers (Stripe/PayPal) in admin')
        self.stdout.write('   2. Create additional subscription plans if needed')
        self.stdout.write('   3. Test the billing flow with a test user')
        self.stdout.write('   4. Monitor user feedback and subscription metrics')
        self.stdout.write('\n💡 Admin URL: /admin/billing/billingsettings/')
        self.stdout.write('💡 Plans URL: /billing/plans/')
        self.stdout.write('='*50)
