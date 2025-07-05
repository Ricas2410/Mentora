from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@Pentora.com').exists():
            User.objects.create_superuser(
                email='admin@Pentora.com',
                username='admin',
                first_name='Admin',
                last_name='User',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created superuser: admin@Pentora.com / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )
