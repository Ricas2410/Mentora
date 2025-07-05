from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from billing.models import BillingSettings, SubscriptionPlan


class Command(BaseCommand):
    help = 'Setup Paystack configuration and update pricing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--public-key',
            type=str,
            help='Paystack public key',
        )
        parser.add_argument(
            '--secret-key',
            type=str,
            help='Paystack secret key',
        )
        parser.add_argument(
            '--test-mode',
            action='store_true',
            help='Enable test mode',
        )
        parser.add_argument(
            '--exchange-rate',
            type=float,
            default=12.0,
            help='USD to GHS exchange rate (default: 12.0)',
        )

    def handle(self, *args, **options):
        self.stdout.write('Setting up Paystack configuration...')
        
        # Get or create billing settings
        settings = BillingSettings.get_settings()
        
        # Update Paystack settings
        settings.paystack_enabled = True
        settings.paystack_test_mode = options.get('test_mode', True)
        settings.base_currency = 'GHS'
        settings.usd_to_ghs_rate = Decimal(str(options['exchange_rate']))
        settings.last_rate_update = timezone.now()
        
        if options.get('public_key'):
            settings.paystack_public_key = options['public_key']
            
        if options.get('secret_key'):
            settings.paystack_secret_key = options['secret_key']
        
        settings.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Paystack configuration updated')
        )
        self.stdout.write(f'   - Test Mode: {settings.paystack_test_mode}')
        self.stdout.write(f'   - Base Currency: {settings.base_currency}')
        self.stdout.write(f'   - Exchange Rate: 1 USD = {settings.usd_to_ghs_rate} GHS')
        
        # Update existing plans with GHS pricing
        self.stdout.write('\nUpdating subscription plans with GHS pricing...')
        
        plans = SubscriptionPlan.objects.all()
        for plan in plans:
            # Calculate GHS prices
            monthly_ghs = plan.monthly_price * settings.usd_to_ghs_rate
            yearly_ghs = plan.yearly_price * settings.usd_to_ghs_rate if plan.yearly_price else None
            
            # Update plan
            plan.monthly_price_ghs = monthly_ghs
            plan.yearly_price_ghs = yearly_ghs
            plan.save()
            
            self.stdout.write(f'   - {plan.name}:')
            self.stdout.write(f'     Monthly: ${plan.monthly_price} → GH₵{monthly_ghs:.2f}')
            if yearly_ghs:
                self.stdout.write(f'     Yearly: ${plan.yearly_price} → GH₵{yearly_ghs:.2f}')
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 Paystack setup complete!'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('1. Add your Paystack keys to the admin panel')
        self.stdout.write('2. Test payments in test mode')
        self.stdout.write('3. Switch to live mode when ready')
        self.stdout.write('\nPaystack webhook URL:')
        self.stdout.write('   https://yourdomain.com/billing/paystack/webhook/')
        self.stdout.write('\nAdmin panel: /admin/billing/billingsettings/1/change/')
