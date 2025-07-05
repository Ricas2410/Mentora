from django.core.management.base import BaseCommand
from billing.models import SubscriptionPlan
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create default subscription plans'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing plans and create new ones',
        )
    
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Deleting existing plans...')
            SubscriptionPlan.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Existing plans deleted'))
        
        self.stdout.write('📋 Creating subscription plans...')
        
        # Free Plan
        free_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Free',
            defaults={
                'description': 'Perfect for getting started with basic learning features',
                'price': Decimal('0.00'),
                'monthly_price': Decimal('0.00'),
                'yearly_price': None,
                'billing_cycle': 'monthly',
                'max_subjects': 3,
                'max_quizzes_per_day': 5,
                'priority_support': False,
                'advanced_analytics': False,
                'offline_access': False,
                'is_active': True,
                'is_featured': False,
                'sort_order': 1,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Free plan'))
        
        # Basic Plan
        basic_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Basic',
            defaults={
                'description': 'Great for individual learners who want more subjects and quizzes',
                'price': Decimal('9.99'),
                'monthly_price': Decimal('9.99'),
                'yearly_price': Decimal('95.90'),  # 20% discount
                'billing_cycle': 'monthly',
                'max_subjects': 10,
                'max_quizzes_per_day': 25,
                'priority_support': False,
                'advanced_analytics': True,
                'offline_access': False,
                'is_active': True,
                'is_featured': False,
                'sort_order': 2,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Basic plan'))
        
        # Premium Plan
        premium_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Premium',
            defaults={
                'description': 'Best for serious learners who want unlimited access and premium features',
                'price': Decimal('19.99'),
                'monthly_price': Decimal('19.99'),
                'yearly_price': Decimal('191.90'),  # 20% discount
                'billing_cycle': 'monthly',
                'max_subjects': None,  # Unlimited
                'max_quizzes_per_day': None,  # Unlimited
                'priority_support': True,
                'advanced_analytics': True,
                'offline_access': True,
                'is_active': True,
                'is_featured': True,
                'sort_order': 3,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Premium plan (Featured)'))
        
        # Annual Premium Plan (with discount)
        annual_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Premium Annual',
            defaults={
                'description': 'Save 20% with our annual premium plan - best value for dedicated learners',
                'price': Decimal('199.99'),  # Legacy field
                'monthly_price': Decimal('199.99'),  # This is actually yearly, but keeping for compatibility
                'yearly_price': Decimal('1919.90'),  # 20% discount from monthly * 12
                'billing_cycle': 'yearly',
                'max_subjects': None,  # Unlimited
                'max_quizzes_per_day': None,  # Unlimited
                'priority_support': True,
                'advanced_analytics': True,
                'offline_access': True,
                'is_active': True,
                'is_featured': False,
                'sort_order': 4,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Premium Annual plan'))

        # Student Plan (discounted)
        student_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Student',
            defaults={
                'description': 'Special pricing for students - all premium features at a student-friendly price',
                'price': Decimal('4.99'),
                'monthly_price': Decimal('4.99'),
                'yearly_price': Decimal('47.90'),  # 20% discount
                'billing_cycle': 'monthly',
                'max_subjects': None,  # Unlimited
                'max_quizzes_per_day': None,  # Unlimited
                'priority_support': False,
                'advanced_analytics': True,
                'offline_access': True,
                'is_active': True,
                'is_featured': False,
                'sort_order': 5,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Created Student plan'))
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 SUBSCRIPTION PLANS CREATED'))
        self.stdout.write('='*50)
        
        plans = SubscriptionPlan.objects.filter(is_active=True).order_by('sort_order')
        for plan in plans:
            featured = " (Featured)" if plan.is_featured else ""
            price = f"${plan.price}" if plan.price > 0 else "Free"
            self.stdout.write(f'📋 {plan.name}{featured}: {price}/{plan.billing_cycle}')
        
        self.stdout.write(f'\n📊 Total active plans: {plans.count()}')
        self.stdout.write('💡 You can modify these plans in the admin panel')
        self.stdout.write('💡 Admin URL: /admin/billing/subscriptionplan/')
        self.stdout.write('='*50)
