from django.core.management.base import BaseCommand
from billing.models import SubscriptionPlan
from subjects.models import Subject
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update subscription plans with yearly pricing and subject allocations'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-subjects',
            action='store_true',
            help='Reset all subject allocations',
        )
    
    def handle(self, *args, **options):
        self.stdout.write('🔄 Updating subscription plans with yearly pricing and subject allocations...')
        
        # Get all subjects
        all_subjects = list(Subject.objects.filter(is_active=True))
        total_subjects = len(all_subjects)
        
        self.stdout.write(f'📚 Found {total_subjects} active subjects')
        
        # Update each plan
        plans_updated = 0
        
        for plan in SubscriptionPlan.objects.all():
            self.stdout.write(f'\n📋 Updating plan: {plan.name}')
            
            # Set yearly pricing (20% discount from monthly * 12)
            if plan.monthly_price > 0:
                yearly_price = plan.monthly_price * 12 * Decimal('0.8')  # 20% discount
                plan.yearly_price = yearly_price
                self.stdout.write(f'   💰 Monthly: ${plan.monthly_price}, Yearly: ${yearly_price} (20% off)')
            
            # Allocate subjects based on plan type
            if options['reset_subjects'] or not plan.allowed_subjects.exists():
                plan.allowed_subjects.clear()
                
                if plan.name.lower() == 'free':
                    # Free plan: First 3 subjects
                    subjects_to_add = all_subjects[:3]
                    plan.max_subjects = 3
                elif plan.name.lower() == 'basic':
                    # Basic plan: First 6 subjects
                    subjects_to_add = all_subjects[:6]
                    plan.max_subjects = 6
                elif plan.name.lower() == 'premium':
                    # Premium plan: All subjects
                    subjects_to_add = all_subjects
                    plan.max_subjects = None
                elif plan.name.lower() == 'student':
                    # Student plan: All subjects
                    subjects_to_add = all_subjects
                    plan.max_subjects = None
                elif 'annual' in plan.name.lower():
                    # Annual plans: All subjects
                    subjects_to_add = all_subjects
                    plan.max_subjects = None
                else:
                    # Default: Half of subjects
                    subjects_to_add = all_subjects[:total_subjects//2]
                    plan.max_subjects = total_subjects//2
                
                plan.save()
                plan.allowed_subjects.set(subjects_to_add)
                
                self.stdout.write(f'   📚 Allocated {len(subjects_to_add)} subjects:')
                for subject in subjects_to_add[:5]:  # Show first 5
                    self.stdout.write(f'      - {subject.name}')
                if len(subjects_to_add) > 5:
                    self.stdout.write(f'      ... and {len(subjects_to_add) - 5} more')
            else:
                plan.save()
                current_subjects = plan.allowed_subjects.count()
                self.stdout.write(f'   📚 Keeping existing {current_subjects} subject allocations')
            
            plans_updated += 1
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('🎉 PLAN UPDATE COMPLETE'))
        self.stdout.write('='*60)
        
        for plan in SubscriptionPlan.objects.filter(is_active=True).order_by('sort_order'):
            monthly = f"${plan.monthly_price}/month"
            yearly = f"${plan.yearly_price}/year" if plan.yearly_price else "No yearly option"
            subjects = plan.subject_count_display
            
            self.stdout.write(f'📋 {plan.name}:')
            self.stdout.write(f'   💰 {monthly} | {yearly}')
            self.stdout.write(f'   📚 {subjects}')
            if plan.yearly_price:
                discount = plan.yearly_discount_percentage
                self.stdout.write(f'   💸 Yearly saves {discount}%')
        
        self.stdout.write(f'\n✅ Updated {plans_updated} plans')
        self.stdout.write('💡 Admin can now manage subject allocations in /admin/billing/subscriptionplan/')
        self.stdout.write('='*60)
