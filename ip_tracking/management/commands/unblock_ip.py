from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Remove an IP address from the blocked list."

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to unblock.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        deleted, _ = BlockedIP.objects.filter(ip_address=ip_address).delete()
        if deleted:
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully unblocked IP: {ip_address}"))
        else:
            self.stdout.write(self.style.WARNING(f"⚠️ IP not found in blocked list: {ip_address}"))
