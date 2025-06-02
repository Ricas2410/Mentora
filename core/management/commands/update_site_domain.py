from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Update the site domain for email verification links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            help='The domain to set (e.g., yourusername.pythonanywhere.com)',
        )
        parser.add_argument(
            '--protocol',
            type=str,
            default='https',
            choices=['http', 'https'],
            help='The protocol to use (http or https, default: https)',
        )

    def handle(self, *args, **options):
        domain = options.get('domain')
        protocol = options.get('protocol', 'https')

        if not domain:
            self.stdout.write(
                self.style.ERROR('Please provide a domain using --domain')
            )
            return

        try:
            # Update the Sites framework
            site = Site.objects.get_current()
            old_domain = site.domain
            site.domain = domain
            site.name = f'Mentora ({domain})'
            site.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated site domain from "{old_domain}" to "{domain}"'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Protocol set to: {protocol}'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'Make sure to update your .env file with:'
                )
            )
            self.stdout.write(f'SITE_DOMAIN={domain}')
            self.stdout.write(f'SITE_PROTOCOL={protocol}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating site domain: {str(e)}')
            )
