"""
Management command to seed the Insight model with sample blog posts.
Run with: python manage.py seed_insights
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from myApp.models import Insight


class Command(BaseCommand):
    help = 'Seed the Insight model with sample blog posts'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Gold Leaf Scapes blog insights...')

        # Get or create a default author
        author, created = User.objects.get_or_create(
            username='blog_author',
            defaults={
                'first_name': 'Karim',
                'last_name': 'Al-Rashid',
                'email': 'karim@goldleafscapes.ae',
            }
        )
        if created:
            author.set_password('temp_password_123')
            author.save()
            self.stdout.write(f'Created author: {author.username}')

        insights_data = [
            {
                'title': 'The Art of Bringing the Desert<br>to <em>Life:</em> Our Design Manifesto',
                'slug': 'design-manifesto',
                'excerpt': 'How Golden Leaf Scapes navigates the tension between Dubai\'s elemental extremes and the human desire for flourishing, living environments.',
                'content': '''<p class="lead" id="section-intro">
      There is a paradox at the heart of our work. The UAE is one of the most inhospitable climates on Earth for the kind of lush, living environments our clients dream of — and yet, for thirteen years, we have built them anyway. Not despite the desert, but in dialogue with it.
    </p>

    <h2 id="section-philosophy">Our Philosophy: Environment as a Living Argument</h2>
    <p>
      A landscape is never passive. Every stone placed, every specimen planted, every pool positioned relative to the prevailing summer wind represents a claim about how humans and nature should coexist. At Golden Leaf Scapes, our design philosophy begins with a rejection of the idea that beauty requires conquest. We do not impose. We negotiate.
    </p>
    <p>
      The UAE's climate — peak summer temperatures exceeding 45°C, humidity levels on the coast that can surpass 90%, and an annual rainfall that rarely exceeds 100mm — is not an obstacle we work around. It is a constraint that sharpens our creativity and demands genuine horticultural intelligence rather than cosmetic landscaping.
    </p>

    <div class="article-img">
      <div class="article-img-inner teal">
        <i class="fas fa-drafting-compass"></i>
      </div>
    </div>
    <p class="img-caption">Design rendering of a recent Emirates Hills estate commission — conceptual phase, 2024.</p>

    <div class="pullquote">
      <p>"We do not design gardens. We engineer living systems — ones that will look better in year five than they do on opening day."</p>
      <cite>— Karim Al-Rashid, Head of Design</cite>
    </div>

    <h2 id="section-principles">The Six Principles We Never Compromise</h2>
    <p>
      Over more than four hundred completed projects, we have distilled our approach to six design principles. These are not aesthetic guidelines — they are structural commitments embedded into every brief we accept.
    </p>

    <h3>1. Climate-First Plant Selection</h3>
    <p>
      Before a single conceptual sketch is drawn, our horticultural team conducts a full microclimate analysis of the site. Wind corridors, shade patterns across different seasons, soil salinity, and drainage gradients all inform which species can genuinely thrive — not merely survive — in a given space.
    </p>
    <ul class="styled">
      <li>Native and naturalized species are always prioritised in the conceptual palette.</li>
      <li>We maintain our own nursery, allowing us to acclimatize specimens over months before installation.</li>
      <li>Every planting plan includes a 24-month establishment protocol with defined success metrics.</li>
    </ul>

    <div class="stat-callout">
      <div class="stat-cell"><div class="num">400+</div><div class="lbl">Projects Completed</div></div>
      <div class="stat-cell"><div class="num">94%</div><div class="lbl">Client Retention Rate</div></div>
      <div class="stat-cell"><div class="num">13yrs</div><div class="lbl">Of Dubai Expertise</div></div>
    </div>

    <h3>2. Water as a Design Material, Not a Resource to Minimise</h3>
    <p>
      This might seem counterintuitive in a water-scarce region. But the way we work with water — through carefully calibrated drip irrigation, evapotranspiration modelling, and the considered placement of water features — is central to how our landscapes feel, not just how they function.
    </p>
    <p>
      The sound of water is one of the most psychologically powerful tools in landscape design. A well-positioned reflecting pool can reduce perceived ambient temperature by several degrees. A narrow rill running beneath a shaded pergola transforms an outdoor corridor from a thoroughfare into a destination.
    </p>

    <div class="article-img">
      <div class="article-img-inner warm">
        <i class="fas fa-water"></i>
      </div>
    </div>
    <p class="img-caption">Water rill installation at a Palm Jumeirah residence. The channel runs 18 metres from terrace to pool level.</p>

    <h3>3. Light Architecture</h3>
    <p>
      In a climate where shade is a luxury, we treat the creation of it as an art form. The angle, density, and material of overhead structures — whether timber pergolas, tensile sails, or mature tree canopies — define whether an outdoor space is genuinely usable or merely decorative.
    </p>

    <h3>4. The Night Garden</h3>
    <p>
      Dubai's outdoor life migrates after dark for six months of the year. A space that performs only in daylight is, in the Gulf context, half a space. Every project we undertake is designed to have an entirely distinct and considered night-time character — one that emerges from the lighting design rather than being imposed upon the planting.
    </p>

    <div class="pullquote">
      <p>"The best outdoor spaces in this region earn their identity after 9pm. If the lighting plan is an afterthought, so is the design."</p>
      <cite>— Sara Al-Mana, Senior Landscape Architect</cite>
    </div>

    <h3>5. Material Memory</h3>
    <p>
      Every material we specify must age well in the Gulf context. Marine-grade stainless steel, hand-selected limestone, teak treated to resist UV degradation, and glazed ceramics that hold their glaze under thermal cycling — these are not luxury specifications. They are the minimum standard required for work that will look better in year ten than it does on the day we hand over the keys.
    </p>

    <h3>6. Silence as a Spatial Value</h3>
    <p>
      In urban Dubai, where the ambient noise of construction and traffic is omnipresent, the capacity of a garden to create genuine acoustic shelter is among its most precious gifts. We use topography, dense planting buffers, and water features not just for their visual qualities, but as instruments of quiet.
    </p>

    <h2 id="section-future">Where We Are Going</h2>
    <p>
      The next frontier in Gulf landscaping is not merely aesthetic — it is ecological. As conversations around urban heat islands, biodiversity corridors, and carbon sequestration become increasingly urgent in regional policy, the landscape profession is being asked to do more than create beautiful spaces. We are being asked to create resilient ones.
    </p>
    <p>
      At Golden Leaf Scapes, we believe that luxury and sustainability are not competing values. The most enduring spaces — the ones that clients call us about a decade after installation to tell us they have never looked better — are the ones designed with genuine ecological intelligence from the outset.
    </p>
    <p>
      That is the work we intend to keep doing. One extraordinary space at a time.
    </p>''',
                'featured_image_url': '',
                'author': author,
                'status': 'published',
                'published_at': timezone.now() - timedelta(days=30),
            },
            {
                'title': 'Infinity Pools in the UAE: Engineering Beauty at the Edge of the Horizon',
                'slug': 'infinity-pools-uae',
                'excerpt': 'From the structural demands of cantilevered edges to the chemical nuances of saltwater systems in Dubai\'s climate — a definitive guide for the discerning homeowner.',
                'content': '''<p class="lead" id="section-intro">
      The infinity pool has become synonymous with luxury residential design in the UAE. But what many homeowners don't realize is that creating a pool that appears to merge seamlessly with the horizon requires far more than aesthetic vision — it demands engineering precision, material science, and an intimate understanding of how water behaves in extreme climates.
    </p>

    <h2 id="section-engineering">The Engineering Challenge</h2>
    <p>
      An infinity edge pool is, fundamentally, a controlled waterfall. The water that appears to vanish into the horizon is actually flowing over a precisely calibrated weir into a catch basin below. This requires a pump system capable of moving thousands of litres per hour, a structural design that can support the weight of water suspended beyond the pool's primary structure, and a finish material that will maintain its integrity under constant water flow and UV exposure.
    </p>

    <div class="article-img">
      <div class="article-img-inner teal">
        <i class="fas fa-water"></i>
      </div>
    </div>
    <p class="img-caption">Infinity edge detail at a Palm Jumeirah villa. The weir extends 12cm beyond the pool structure.</p>

    <h2 id="section-climate">Climate Considerations</h2>
    <p>
      Dubai's climate presents unique challenges for pool design. Evaporation rates can exceed 5mm per day during peak summer months, meaning a typical residential pool can lose 150-200 litres daily. This isn't just a water consumption issue — it affects chemical balance, pump efficiency, and the structural integrity of the pool shell itself.
    </p>

    <div class="stat-callout">
      <div class="stat-cell"><div class="num">5mm</div><div class="lbl">Daily Evaporation</div></div>
      <div class="stat-cell"><div class="num">45°C</div><div class="lbl">Peak Water Temp</div></div>
      <div class="stat-cell"><div class="num">24/7</div><div class="lbl">Filtration Required</div></div>
    </div>

    <h3>Saltwater vs. Chlorine Systems</h3>
    <p>
      The choice between saltwater and traditional chlorine systems is one of the most consequential decisions in pool design. Saltwater pools use electrolysis to generate chlorine from salt, creating a softer, more natural-feeling water. However, they require more sophisticated equipment and can be more corrosive to certain materials.
    </p>

    <h2 id="section-materials">Material Selection</h2>
    <p>
      The finish material of an infinity pool is not merely aesthetic — it's a performance specification. In the UAE, we specify materials that can withstand:
    </p>
    <ul class="styled">
      <li>Constant UV exposure (the pool receives direct sunlight for 8-10 hours daily)</li>
      <li>Thermal cycling (water temperature can fluctuate 15°C between day and night)</li>
      <li>Chemical exposure (both chlorine and saltwater systems are corrosive)</li>
      <li>High humidity (which accelerates material degradation)</li>
    </ul>

    <p>
      Our preferred finish is a combination of glass mosaic tiles for the waterline and polished natural stone for the decking. This combination provides both visual elegance and long-term durability.
    </p>

    <h2 id="section-maintenance">Maintenance Philosophy</h2>
    <p>
      A well-designed infinity pool should require minimal maintenance, not despite its complexity, but because of it. Automated chemical dosing systems, variable-speed pumps that adjust to load, and intelligent filtration that runs continuously but efficiently — these are not luxury add-ons. They are essential components of a pool that will perform flawlessly for decades.
    </p>''',
                'featured_image_url': '',
                'author': author,
                'status': 'published',
                'published_at': timezone.now() - timedelta(days=45),
            },
            {
                'title': 'Five Landscaping Mistakes Dubai Villa Owners Make (And How to Avoid Them)',
                'slug': 'landscaping-mistakes-dubai',
                'excerpt': 'After 13 years and over 400 completed projects, our lead designers share the most common — and costly — landscaping missteps they encounter on new client sites.',
                'content': '''<p class="lead" id="section-intro">
      Over thirteen years of designing and installing landscapes across Dubai, we've seen the same mistakes repeated time and again. These aren't minor oversights — they're fundamental errors in approach that can cost homeowners tens of thousands of dirhams in premature replacements, excessive maintenance, and complete redesigns.
    </p>

    <h2 id="section-mistake1">Mistake #1: Choosing Plants Based on Appearance Alone</h2>
    <p>
      The most common mistake we see is selecting plants based purely on how they look in a nursery or in photographs, without considering whether they can actually thrive in the specific microclimate of the site. A plant that flourishes in a shaded, irrigated nursery may struggle in full sun with minimal water.
    </p>
    <p>
      <strong>The Solution:</strong> Always begin with a site analysis. Understand the sun patterns, wind corridors, soil composition, and drainage characteristics of your specific location. Then select plants that are proven performers in those exact conditions.
    </p>

    <h2 id="section-mistake2">Mistake #2: Underestimating Irrigation Needs</h2>
    <p>
      Many homeowners assume that once a landscape is established, it will require minimal water. In Dubai's climate, this is rarely true. Even drought-tolerant species need consistent irrigation during their establishment period (typically 18-24 months), and many will require ongoing supplemental water during peak summer months.
    </p>

    <div class="pullquote">
      <p>"The most expensive irrigation system is the one that doesn't work properly. Invest in quality from the start."</p>
      <cite>— Mohammed Hassan, Irrigation Specialist</cite>
    </div>

    <h2 id="section-mistake3">Mistake #3: Ignoring Drainage</h2>
    <p>
      Dubai receives minimal annual rainfall, but when it does rain, it often comes in intense bursts. Without proper drainage, water can pool around foundations, damage hardscaping, and drown plants. We've seen entire landscapes fail because drainage was treated as an afterthought.
    </p>

    <h2 id="section-mistake4">Mistake #4: Skimping on Hardscaping Materials</h2>
    <p>
      The Gulf climate is brutal on materials. UV degradation, thermal expansion and contraction, salt exposure, and high humidity can destroy inferior materials within a few years. What seems like a cost-saving measure in year one becomes an expensive replacement project in year five.
    </p>

    <div class="stat-callout">
      <div class="stat-cell"><div class="num">5x</div><div class="lbl">UV Exposure vs. Europe</div></div>
      <div class="stat-cell"><div class="num">45°C</div><div class="lbl">Surface Temp Range</div></div>
      <div class="stat-cell"><div class="num">90%</div><div class="lbl">Peak Humidity</div></div>
    </div>

    <h2 id="section-mistake5">Mistake #5: Designing Without a Maintenance Plan</h2>
    <p>
      A landscape is not a static installation — it's a living system that requires ongoing care. Many homeowners design beautiful spaces without considering who will maintain them, how often maintenance is needed, and what the ongoing costs will be. The result is landscapes that look stunning on day one but deteriorate rapidly.
    </p>

    <p>
      <strong>The Solution:</strong> Design with maintenance in mind from the beginning. Choose plants that require similar care schedules, create access paths for maintenance equipment, and plan for seasonal variations in care requirements.
    </p>''',
                'featured_image_url': '',
                'author': author,
                'status': 'published',
                'published_at': timezone.now() - timedelta(days=60),
            },
        ]

        created_count = 0
        updated_count = 0

        for data in insights_data:
            insight, created = Insight.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'excerpt': data['excerpt'],
                    'content': data['content'],
                    'featured_image_url': data['featured_image_url'],
                    'author': data['author'],
                    'status': data['status'],
                    'published_at': data['published_at'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {insight.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Updated: {insight.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Seeding complete! Created {created_count} new insights, updated {updated_count} existing insights.'
        ))

