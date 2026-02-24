"""
Master management command to seed all models with initial data.
Run with: python manage.py seed_all

This command runs all seed scripts in the correct order:
1. Hero data
2. Services (and ProcessSteps)
3. Projects (requires Services)
4. Insights (blog posts)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Seed all models with initial data (Hero, Services, Projects, Insights)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-hero',
            action='store_true',
            help='Skip seeding hero data',
        )
        parser.add_argument(
            '--skip-services',
            action='store_true',
            help='Skip seeding services data',
        )
        parser.add_argument(
            '--skip-projects',
            action='store_true',
            help='Skip seeding projects data',
        )
        parser.add_argument(
            '--skip-insights',
            action='store_true',
            help='Skip seeding insights data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🌱 Starting database seeding process...\n'))
        
        # Seed Hero data
        if not options['skip_hero']:
            self.stdout.write(self.style.WARNING('📋 Seeding Hero data...'))
            try:
                call_command('seed_hero')
                self.stdout.write(self.style.SUCCESS('✓ Hero data seeded\n'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error seeding hero: {e}\n'))
        else:
            self.stdout.write(self.style.WARNING('⏭ Skipping Hero data\n'))

        # Seed Services (includes ProcessSteps)
        if not options['skip_services']:
            self.stdout.write(self.style.WARNING('📋 Seeding Services and ProcessSteps...'))
            try:
                call_command('seed_services')
                self.stdout.write(self.style.SUCCESS('✓ Services and ProcessSteps seeded\n'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error seeding services: {e}\n'))
        else:
            self.stdout.write(self.style.WARNING('⏭ Skipping Services data\n'))

        # Seed Projects (requires Services to exist)
        if not options['skip_projects']:
            self.stdout.write(self.style.WARNING('📋 Seeding Projects...'))
            try:
                call_command('seed_projects')
                self.stdout.write(self.style.SUCCESS('✓ Projects seeded\n'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error seeding projects: {e}\n'))
        else:
            self.stdout.write(self.style.WARNING('⏭ Skipping Projects data\n'))

        # Seed Insights (blog posts)
        if not options['skip_insights']:
            self.stdout.write(self.style.WARNING('📋 Seeding Insights (blog posts)...'))
            try:
                call_command('seed_insights')
                self.stdout.write(self.style.SUCCESS('✓ Insights seeded\n'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error seeding insights: {e}\n'))
        else:
            self.stdout.write(self.style.WARNING('⏭ Skipping Insights data\n'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding complete!\n'))
        self.stdout.write(self.style.SUCCESS('Your database is now populated with sample data.'))
        self.stdout.write(self.style.SUCCESS('You can now run migrations and start using the dashboard.\n'))

