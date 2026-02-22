"""
Management command to seed the Project model with sample portfolio projects.
Run with: python manage.py seed_projects
"""

from django.core.management.base import BaseCommand
from myApp.models import Project, Service


class Command(BaseCommand):
    help = 'Seed the Project model with sample portfolio projects'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Gold Leaf Scapes portfolio projects...')

        # Get services for relationships
        villa_service = Service.objects.filter(slug='villa-landscaping').first()
        commercial_service = Service.objects.filter(slug='commercial-landscapes').first()
        pool_service = Service.objects.filter(slug='swimming-pool-design').first()
        pergola_service = Service.objects.filter(slug='pergolas-pavilions').first()

        projects_data = [
            {
                'title': 'The Verdant Villa',
                'slug': 'verdant-villa',
                'location': 'Dubai Hills Estate',
                'category': 'Villa Landscaping + Pool',
                'short_description': 'A luxurious tropical garden transformation featuring custom pool design, lush planting, and elegant outdoor living spaces.',
                'full_description': """This stunning villa transformation in Dubai Hills Estate represents the pinnacle of residential landscape design. The project began with a comprehensive site analysis, understanding the unique microclimate, soil conditions, and the client's vision for a tropical paradise.

Our design team created a seamless flow between indoor and outdoor spaces, incorporating a custom infinity-edge pool that appears to merge with the horizon. The planting scheme features a carefully curated selection of tropical and desert-adapted species, creating layers of texture and color that evolve throughout the seasons.

Key highlights include:
• Custom-designed infinity pool with integrated spa
• Extensive hardscaping using premium natural stone
• Smart irrigation system with moisture sensors
• Architectural LED lighting for night-time ambiance
• Mature palm trees and tropical foliage
• Outdoor kitchen and dining area
• Private garden retreat with pergola

The project was completed in 8 weeks, with meticulous attention to every detail. The result is a private oasis that serves as both a family retreat and an impressive entertainment space.""",
                'specs_data': 'Area|850 sqm,Completion|2024,Style|Tropical Modern,Duration|8 Weeks,Plants|120+ Specimens,Features|Infinity Pool, Outdoor Kitchen, Pergola',
                'gallery_images': '',  # Will be populated with Cloudinary URLs when images are uploaded
                'related_service': villa_service,
                'featured': True,
                'order': 1,
            },
            {
                'title': 'Azure Corporate Garden',
                'slug': 'azure-corporate-garden',
                'location': 'DIFC, Dubai',
                'category': 'Commercial Landscaping',
                'short_description': 'A sophisticated corporate plaza design that elevates the building\'s prestige while creating a welcoming environment for employees and visitors.',
                'full_description': """This commercial landscaping project in DIFC required a design that would reflect the corporate identity while creating a biophilic environment that enhances well-being and productivity.

The design incorporates:
• Modern geometric planting beds with drought-tolerant species
• Water feature as a focal point
• Premium hardscaping materials
• Integrated seating areas for outdoor meetings
• Smart irrigation and lighting systems
• Low-maintenance plant selection for sustainability

The project was executed in phases to minimize disruption to building operations, with careful coordination between our team, the building management, and municipal authorities.""",
                'specs_data': 'Area|1,200 sqm,Completion|2024,Style|Contemporary Corporate,Duration|10 Weeks,Plants|200+ Specimens,Features|Water Feature, Seating Areas, Smart Systems',
                'gallery_images': '',
                'related_service': commercial_service,
                'featured': True,
                'order': 2,
            },
            {
                'title': 'Amber Terrace Retreat',
                'slug': 'amber-terrace-retreat',
                'location': 'Palm Jumeirah',
                'category': 'Outdoor Living + Pergola',
                'short_description': 'An elegant terrace transformation featuring a custom pergola, outdoor kitchen, and seamless integration with the stunning Palm Jumeirah views.',
                'full_description': """This Palm Jumeirah terrace project showcases how thoughtful design can maximize outdoor living potential. The client wanted a space that would work year-round, providing shade in summer and open views in winter.

Our solution included:
• Custom-designed timber pergola with automated louvered roof
• Integrated outdoor kitchen with premium appliances
• Fire pit area for cooler evenings
• Container planting with Mediterranean species
• Weather-resistant furniture and accessories
• Smart lighting and sound system

The pergola's automated louvered roof allows the space to adapt to weather conditions, providing shade when needed while maintaining the stunning views of the Arabian Gulf.""",
                'specs_data': 'Area|180 sqm,Completion|2024,Style|Mediterranean Modern,Duration|6 Weeks,Features|Automated Pergola, Outdoor Kitchen, Fire Pit',
                'gallery_images': '',
                'related_service': pergola_service,
                'featured': True,
                'order': 3,
            },
            {
                'title': 'The Oasis Pool Garden',
                'slug': 'oasis-pool-garden',
                'location': 'Jumeirah Village',
                'category': 'Swimming Pool + Interior Green',
                'short_description': 'A complete garden transformation featuring a custom pool design, lush landscaping, and interior greening elements that bring nature inside.',
                'full_description': """This comprehensive project combined exterior landscaping with interior greening, creating a cohesive design language throughout the property.

Exterior features:
• Custom freeform pool with integrated spa
• Tropical garden with mature palms
• Outdoor shower and changing area
• Pool deck with non-slip surface
• Landscape lighting for evening ambiance

Interior features:
• Living wall in the main living area
• Preserved moss art installation
• Strategic plant placement throughout
• Biophilic design principles

The result is a seamless connection between indoor and outdoor spaces, with nature integrated throughout the home.""",
                'specs_data': 'Area|600 sqm,Completion|2024,Style|Tropical Oasis,Duration|7 Weeks,Pool Size|8m x 4m,Interior Green|Living Wall + Moss Art',
                'gallery_images': '',
                'related_service': pool_service,
                'featured': True,
                'order': 4,
            },
        ]

        created_count = 0
        updated_count = 0

        for project_data in projects_data:
            project, created = Project.objects.update_or_create(
                slug=project_data['slug'],
                defaults=project_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {project.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {project.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Seeding complete! Created: {created_count}, Updated: {updated_count}'
        ))

