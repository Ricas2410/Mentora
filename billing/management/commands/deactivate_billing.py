from django.core.management.base import BaseCommand
from billing.models import BillingSettings


class Command(BaseCommand):
    help = 'Deactivate billing system (make platform free for all users)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--hide-announcement',
            action='store_true',
            help='Hide the billing announcement banner',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to deactivate billing',
        )
    
    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(self.style.ERROR('❌ Please use --confirm to confirm billing deactivation'))
            self.stdout.write('   This will make the platform free for all users.')
            return
        
        self.stdout.write(self.style.WARNING('⚠️  Deactivating billing system...'))
        
        # Get billing settings
        billing_settings = BillingSettings.get_settings()
        
        # Deactivate billing
        billing_settings.billing_enabled = False
        
        if options['hide_announcement']:
            billing_settings.show_billing_announcement = False
        
        billing_settings.save()
        
        self.stdout.write(self.style.SUCCESS('✅ Billing system deactivated'))
        self.stdout.write('   - All users now have unlimited access')
        self.stdout.write('   - Subscription checks are bypassed')
        self.stdout.write('   - Payment processing is disabled')
        
        if options['hide_announcement']:
            self.stdout.write('   - Billing announcement banner hidden')
        
        self.stdout.write('\n💡 To reactivate billing, use: python manage.py activate_billing')
        self.stdout.write('💡 Existing subscriptions are preserved and will resume when billing is reactivated')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 BILLING DEACTIVATION COMPLETE'))
        self.stdout.write('='*50)
