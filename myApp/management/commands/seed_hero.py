"""
Management command to seed the Hero model with initial data.
Run with: python manage.py seed_hero
"""
from django.core.management.base import BaseCommand
from myApp.models import Hero


class Command(BaseCommand):
    help = 'Seed the Hero model with initial home page hero data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding hero data...')
        
        # Create or update home hero
        hero, created = Hero.objects.update_or_create(
            page='home',
            defaults={
                'eyebrow': "Dubai's Premier Outdoor & Interior Studio",
                'title': "Where Nature Meets<br><em>Refined</em> Living",
                'subtitle': "Gold Leaf Scapes crafts extraordinary outdoor landscapes and bespoke interiors for Dubai's most distinguished residences and commercial spaces.",
                'cta_text': 'View Our Work',
                'cta_link': '#portfolio',
                'secondary_cta_text': 'Request Consultation',
                'secondary_cta_link': '#cta',
                'stats_data': '3+|Years in Dubai,340+|Projects Completed,98%|Client Satisfaction',
                'active': True,
                'order': 0,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created home hero: {hero}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Updated home hero: {hero}'))
        
        self.stdout.write(self.style.SUCCESS('\nHero data seeded successfully!'))

