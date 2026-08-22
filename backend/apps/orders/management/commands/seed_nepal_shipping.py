from django.core.management.base import BaseCommand
from apps.brands.models import Brand
from apps.orders.models import ShippingZone

class Command(BaseCommand):
    help = 'Seeds standard Nepal shipping zones based on real logistics provider coverage (Upaya, Pathao, NCM).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--brand',
            type=str,
            help='Specify a brand slug to only seed for that brand. If omitted, seeds for all ACTIVE brands.',
        )

    def handle(self, *args, **options):
        brand_slug = options['brand']

        if brand_slug:
            brands = Brand.objects.filter(slug=brand_slug)
            if not brands.exists():
                self.stderr.write(self.style.ERROR(f"Brand with slug '{brand_slug}' not found."))
                return
        else:
            brands = Brand.objects.filter(status='ACTIVE')

        if not brands.exists():
            self.stdout.write(self.style.WARNING("No active brands found to seed shipping zones."))
            return

        # Real standard Nepal logistics rates based on 1kg parcel average
        zones_data = [
            {
                "name": "Inside Kathmandu Valley",
                "rate": 100.00,
                "estimated_days": "1-2 days",
                "is_free_above": 3000.00
            },
            {
                "name": "Outside Valley (Bagmati)",
                "rate": 150.00,
                "estimated_days": "2-3 days",
                "is_free_above": 5000.00
            },
            {
                "name": "Province 1 (Koshi) / Biratnagar, Dharan",
                "rate": 200.00,
                "estimated_days": "2-4 days",
                "is_free_above": None
            },
            {
                "name": "Province 2 (Madhesh) / Birgunj, Janakpur",
                "rate": 200.00,
                "estimated_days": "2-4 days",
                "is_free_above": None
            },
            {
                "name": "Gandaki Province / Pokhara",
                "rate": 200.00,
                "estimated_days": "2-4 days",
                "is_free_above": 5000.00
            },
            {
                "name": "Lumbini Province / Butwal, Bhairahawa",
                "rate": 250.00,
                "estimated_days": "3-5 days",
                "is_free_above": None
            },
            {
                "name": "Karnali Province / Surkhet",
                "rate": 300.00,
                "estimated_days": "4-7 days",
                "is_free_above": None
            },
            {
                "name": "Sudurpashchim Province / Dhangadhi",
                "rate": 300.00,
                "estimated_days": "4-7 days",
                "is_free_above": None
            },
        ]

        total_created = 0
        for brand in brands:
            self.stdout.write(f"Seeding zones for {brand.name}...")
            
            # Delete existing to prevent duplicates if running multiple times
            ShippingZone.objects.filter(brand=brand).delete()
            
            for zone_kwargs in zones_data:
                ShippingZone.objects.create(
                    brand=brand,
                    is_active=True,
                    **zone_kwargs
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_created} Nepal shipping zones across {brands.count()} brand(s).'))
