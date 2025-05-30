from django.core.management.base import BaseCommand
from core.models import HeroSection, SiteStatistic


class Command(BaseCommand):
    help = 'Setup initial data for hero section and site statistics'

    def handle(self, *args, **options):
        # Create default hero section if none exists
        if not HeroSection.objects.exists():
            hero = HeroSection.objects.create(
                title="An Easy Way to Learn and Grow",
                subtitle="No matter your background",
                description="Quality education for everyone. Start your learning journey today with our comprehensive, mobile-friendly platform designed specifically for Ghanaian learners.",
                cta_text="Get Started Free",
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created hero section: {hero.title}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Hero section already exists')
            )

        # Create default site statistics if none exist
        if not SiteStatistic.objects.exists():
            stats = [
                {
                    'label': 'Free Forever',
                    'value': '100%',
                    'icon': 'fas fa-heart',
                    'order': 1
                },
                {
                    'label': 'Mobile Friendly',
                    'value': '',
                    'icon': 'fas fa-mobile-alt',
                    'order': 2
                },
                {
                    'label': 'Made for Ghana',
                    'value': '',
                    'icon': 'fas fa-flag',
                    'order': 3
                }
            ]
            
            for stat_data in stats:
                stat = SiteStatistic.objects.create(**stat_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Created statistic: {stat.label}')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Site statistics already exist')
            )

        self.stdout.write(
            self.style.SUCCESS('Initial data setup completed!')
        )
