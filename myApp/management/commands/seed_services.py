"""
Management command to seed the Service model with SEO-optimized data.
Run with: python manage.py seed_services
"""

from django.core.management.base import BaseCommand
from myApp.models import Service, ProcessStep


class Command(BaseCommand):
    help = 'Seed the Service model with premium SEO-optimized service data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Gold Leaf Scapes premium services...')

        services_data = [
            # ==========================================================
            # 1️⃣ VILLA LANDSCAPING (FULLY OPTIMIZED)
            # ==========================================================
            {
                'title': 'Villa &<br><em>Residential</em><br>Landscaping',
                'slug': 'villa-landscaping',
                'short_description': 'Transforming private residences with bespoke garden design, luxury planting schemes, and sculptural water features tailored to the Dubai climate.',
                'full_description': 'Complete villa landscaping services from design to handover.',
                'icon': 'fa-tree',
                'hero_tag': 'Outdoor Landscaping',
                'hero_meta_projects': '140+',
                'hero_meta_satisfaction': '4.9 ★',
                'hero_meta_guarantee': '2 Yrs',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '140+|Villas Transformed|Across Dubai, Abu Dhabi & Sharjah,3–8|Weeks to Completion|Depending on project scope,100%|Custom Designed|No template gardens — ever,2yr|Craftsmanship Guarantee|Plants, structures & systems',
                'overview_content': """Dubai's villa gardens are more than outdoor space — they are an extension of your home's identity and a private retreat from the world outside. At Gold Leaf Scapes, we approach every residential project as a unique canvas requiring deep thought about <strong>how you live, entertain, and unwind.</strong>

Our landscape architects begin every project with extensive site analysis: soil composition, sun trajectories, prevailing winds, and proximity to neighbouring properties all inform a design that is not only beautiful but <strong>climatically intelligent</strong> — perfectly adapted to Dubai's heat and evolving seasons.

From lush tropical gardens evoking Balinese resort aesthetics, to sleek desert-modern designs that celebrate UAE's native flora — we execute every concept with meticulous attention to detail. No project is completed until <strong>every element is perfect.</strong>

We handle everything: site clearance, civil works, irrigation, softscaping, hardscaping, lighting, and final planting — delivering a complete, move-in ready garden that exceeds expectation.""",
                'whats_included': """On-site consultation & site analysis
Concept design & mood boards
Full 3D render & walkthrough
Planting specification & sourcing
Hardscaping (paths, decks, edging)
Smart drip irrigation system
Landscape lighting design & install
Soil preparation & amendments
Full planting & establishment
2-year guarantee & aftercare guide""",
                'timeline_data': 'Week 1|Site survey, design brief & concept development,Week 2|3D visualization, revisions & final design sign-off,Week 3–5|Civil works, hardscaping & irrigation installation,Week 6–7|Planting, lighting install & final dressing,Week 8|Snagging, handover & care briefing',
                'process_steps_data': 'fa-search|Discovery & Site Analysis|We spend time understanding how you live. A thorough site survey captures soil data, drainage, sun exposure, and existing features that inform every design decision.,fa-paint-brush|Concept & Mood Boarding|Our designers curate material palettes, planting schemes, and spatial layouts — presenting 2-3 distinct concepts for you to choose from and refine together.,fa-vr-cardboard|3D Visualization|Before any soil is turned, experience your garden in photorealistic 3D — walkthroughs, seasonal plant simulations, and lighting previews at night and day.,fa-tools|Civil & Structural Works|Our civil team handles groundworks, drainage, pathways, edging, raised beds, retaining walls, and structural features — built to the highest standard.,fa-seedling|Planting & Establishment|We source and plant every specimen ourselves — from statement palms to ground-cover perennials — and include a 30-day plant establishment check-up.,fa-key|Handover & Ongoing Care|A detailed care guide, irrigation programming session, and optional monthly maintenance plan ensure your garden thrives for years to come.',
                'showcase_projects_data': 'Dubai Hills Estate|The Palm Residence Garden|large,Arabian Ranches 2|Infinity Pool Terrace|small,Palm Jumeirah|Shaded Pergola Terrace|half,Jumeirah Golf Estates|Formal Garden with Pool|half',
                'specs_data': 'Minimum Plot|200 sqm (smaller projects case-by-case),Design Style|Tropical, Contemporary, Desert-Modern, Formal, Cottage — all styles,Plants|Climate-adapted species; sourced locally & imported on request,Hardscaping|Natural stone, porcelain, timber decking, exposed aggregate, gravel,Irrigation|Smart drip + micro-spray; app-controlled; moisture-sensor ready,Lighting|LED architectural; uplighting, path, underwater — all programmable,Guarantee|2-year structural & planting guarantee; extended on request,Maintenance|Optional monthly, quarterly, or annual care plans available',
                'faq_data': 'How long does a typical villa garden take?|Most residential villa gardens are completed within 4–8 weeks from design sign-off, depending on plot size and complexity. We provide a detailed project timeline at the quotation stage.,Do you work during summer months?|Yes. Our team is experienced working in Dubai\'s summer heat and we adapt our scheduling — typically starting early morning — to ensure quality is never compromised. We also time planting for optimal establishment success.,Can I see my design before work starts?|Absolutely. Every project includes a full 3D visualization — photorealistic renders, a walkthrough video, and day/night lighting simulations — so you experience your garden before any work begins. Revisions are included.,What areas of Dubai do you cover?|We serve all areas across Dubai, Abu Dhabi, and Sharjah — including Dubai Hills, Arabian Ranches, Palm Jumeirah, JVC, MBR City, Meydan, Damac Hills, and all premium villa communities.,Do you offer ongoing maintenance after completion?|Yes. We offer flexible maintenance plans — monthly, bi-monthly, or quarterly visits covering pruning, fertilising, irrigation adjustment, seasonal planting, and general health checks.,What is included in your 2-year guarantee?|Our guarantee covers all structural elements (walls, pathways, irrigation), lighting installations, and specified plants. If a plant fails under normal care conditions within 2 years, we replace it at no charge.',
                'testimonial_text': 'I handed Gold Leaf Scapes an overgrown plot and they gave me back a garden that stops guests in their tracks. The 3D walkthrough was uncanny — the real thing looks exactly as promised. Worth every dirham.',
                'testimonial_author': 'Khalid Al Rashidi',
                'testimonial_role': 'Villa Owner — Jumeirah Golf Estates, Dubai',
                'related_services': 'swimming-pool-design,pergolas-pavilions,garden-maintenance',
                'featured': True,
                'order': 1,
            },

            # ==========================================================
            # 2️⃣ COMMERCIAL LANDSCAPES
            # ==========================================================
            {
                'title': 'Commercial<br><em>Landscapes</em>',
                'slug': 'commercial-landscapes',
                'short_description': 'Elevating hotels, corporate campuses, retail destinations, and master communities with design-led outdoor environments that make powerful impressions.',
                'full_description': 'Large-scale commercial landscaping for hotels, developers, and corporate properties.',
                'icon': 'fa-building',
                'hero_tag': 'Commercial Landscaping',
                'hero_meta_projects': '85+',
                'hero_meta_satisfaction': '4.8 ★',
                'hero_meta_guarantee': '3 Yrs',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '85+|Commercial Projects|Hotels, Retail & Corporate,6–12|Weeks Build Time|Large-scale projects,100%|Brand-Aligned|Design reflects your identity,3yr|Commercial Guarantee|Structures & systems',
                'overview_content': """Commercial landscapes in Dubai must command attention, reflect brand identity, and deliver long-term value. Gold Leaf Scapes specializes in large-scale commercial landscaping that makes powerful first impressions.

We understand that commercial projects require:
• Coordination with architects and developers
• Compliance with municipal regulations
• Budget management and value engineering
• Phased construction for operational continuity
• Long-term maintenance planning

Our commercial portfolio includes hotel courtyards, retail plazas, corporate headquarters, master communities, and mixed-use developments across the UAE.

From initial concept through to ongoing maintenance, we manage every detail to ensure your commercial landscape becomes a signature asset that elevates your property's prestige and value.""",
                'whats_included': """Site analysis & feasibility study
Master planning & design development
Municipal approval coordination
Phased construction management
Large-scale planting & establishment
Commercial irrigation systems
Architectural lighting design
Hardscape & paving installation
Maintenance program development
3-year commercial guarantee""",
                'timeline_data': 'Week 1–2|Site analysis, design brief & master planning,Week 3–4|Design development, approvals & value engineering,Week 5–8|Phase 1: Civil works & infrastructure,Week 9–12|Phase 2: Hardscaping & planting,Week 13–14|Final installation, commissioning & handover',
                'process_steps_data': 'fa-clipboard-list|Project Brief & Analysis|We analyze your brand, target audience, and operational requirements to create a landscape strategy that aligns with your business goals.,fa-drafting-compass|Master Planning|Our design team creates comprehensive master plans that integrate with architecture, traffic flow, and operational needs.,fa-file-contract|Approvals & Coordination|We handle all municipal approvals and coordinate with architects, MEP consultants, and contractors for seamless execution.,fa-tools|Phased Construction|Our project managers execute construction in phases to minimize disruption to your operations while maintaining quality standards.,fa-seedling|Planting & Softscaping|Large-scale planting programs with climate-adapted species selected for durability and visual impact in commercial settings.,fa-handshake|Handover & Maintenance|Comprehensive handover documentation and flexible maintenance contracts to protect your landscape investment.',
                'showcase_projects_data': 'DIFC|Corporate Plaza Gardens|large,Dubai Marina|Retail Waterfront|small,JBR|Hotel Courtyard|half,Business Bay|Mixed-Use Development|half',
                'specs_data': 'Project Scale|500 sqm to 50,000+ sqm,Design Approach|Brand-aligned, visitor-focused, operational efficiency,Plants|Drought-tolerant, low-maintenance commercial species,Hardscaping|Premium materials: natural stone, porcelain, composite decking,Irrigation|Automated commercial systems with smart controls,Lighting|Architectural LED systems for safety and ambiance,Guarantee|3-year structural guarantee; extended warranties available,Maintenance|Flexible contracts: monthly, quarterly, or annual programs',
                'faq_data': 'What is the typical timeline for commercial projects?|Commercial landscaping projects typically take 6–12 weeks depending on scale and complexity. We provide detailed project schedules with phased milestones.,Do you work with developers and architects?|Yes. We regularly collaborate with leading architects, developers, and consultants in Dubai. We coordinate seamlessly with your project team.,Can you work around operational schedules?|Absolutely. We plan construction phases to minimize disruption. We can work evenings, weekends, or in specific zones to keep your business running.,What maintenance do commercial landscapes require?|Commercial landscapes need regular maintenance for health and appearance. We offer flexible maintenance contracts tailored to your budget and requirements.,Do you handle municipal approvals?|Yes. We manage all landscape-related municipal approvals and ensure compliance with Dubai Municipality and developer requirements.,What areas do you serve?|We serve all commercial projects across Dubai, Abu Dhabi, and Sharjah — from DIFC to JBR, Business Bay to Dubai Marina.',
                'testimonial_text': 'Gold Leaf Scapes transformed our hotel courtyard into a biophilic oasis that guests photograph constantly. The team managed the project flawlessly around our operations — professional, creative, and reliable.',
                'testimonial_author': 'James Thornton',
                'testimonial_role': 'General Manager, Boutique Hotel – DIFC',
                'related_services': 'villa-landscaping,interior-greening,garden-maintenance',
                'featured': True,
                'order': 2,
            },

            # ==========================================================
            # 3️⃣ POOL & WATER FEATURES
            # ==========================================================
            {
                'title': 'Pool & Water<br><em>Features</em>',
                'slug': 'swimming-pool-design',
                'short_description': 'Custom-designed pools, infinity edges, water walls, and reflection pools with smart filtration systems engineered for desert luxury.',
                'full_description': 'Luxury swimming pool design and water feature installation.',
                'icon': 'fa-swimming-pool',
                'hero_tag': 'Water Features',
                'hero_meta_projects': '120+',
                'hero_meta_satisfaction': '4.9 ★',
                'hero_meta_guarantee': '5 Yrs',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '120+|Pools Completed|Infinity, Lap & Plunge,4–10|Weeks Build Time|Design to completion,100%|Custom Designed|Every pool is unique,5yr|Structural Guarantee|Pool shell & systems',
                'overview_content': """A luxury swimming pool is the centerpiece of any premium Dubai property. Gold Leaf Scapes designs and builds custom pools that combine stunning aesthetics with engineering excellence.

Our pool design philosophy:
• Every pool is custom-designed for your space and lifestyle
• Integration with landscape architecture is seamless
• Smart filtration and heating systems for year-round enjoyment
• Safety features built-in from the start
• Energy-efficient systems that reduce operating costs

From infinity-edge pools with panoramic views to compact plunge pools for urban villas, we create water features that become the focal point of your outdoor living space.

Our team handles everything: design, engineering, construction, tiling, filtration installation, and final commissioning — delivering a pool that exceeds expectations.""",
                'whats_included': """Pool design & 3D visualization
Structural engineering & approvals
Excavation & shell construction
Premium tiling & coping installation
Smart filtration system
Heating & temperature control
LED underwater lighting
Water feature integration
Safety features & compliance
5-year structural guarantee""",
                'timeline_data': 'Week 1|Design consultation & site survey,Week 2|3D design, engineering & approvals,Week 3–5|Excavation, shell construction & waterproofing,Week 6–7|Tiling, coping & water features,Week 8–9|Filtration, heating & lighting installation,Week 10|Commissioning, water testing & handover',
                'process_steps_data': 'fa-ruler-combined|Design & Engineering|We design your pool to complement your landscape, optimize space, and meet all safety and structural requirements.,fa-shovel|Excavation & Shell|Our experienced team excavates and constructs the pool shell using reinforced concrete for maximum durability.,fa-tint|Waterproofing & Tiling|Premium waterproofing systems and luxury tiles create a pool that is both beautiful and long-lasting.,fa-cog|Systems Installation|Smart filtration, heating, and LED lighting systems are installed and programmed for optimal performance.,fa-water|Water Features|Waterfalls, cascades, and fountains are integrated seamlessly into your pool design.,fa-check-circle|Commissioning|Final water testing, system programming, and comprehensive handover ensure your pool is ready to enjoy.',
                'showcase_projects_data': 'Palm Jumeirah|Infinity Edge Pool|large,Dubai Hills|Lap Pool & Spa|small,Emirates Hills|Plunge Pool|half,Jumeirah|Waterfall Feature|half',
                'specs_data': 'Pool Types|Infinity, Lap, Plunge, Freeform, Geometric,Size Range|Small plunge pools to Olympic-length lap pools,Depth Options|Shallow lounging areas to deep-end diving,Heating|Solar, heat pump, or gas heating systems,Filtration|Sand, cartridge, or advanced UV systems,Lighting|LED color-changing underwater & perimeter lighting,Guarantee|5-year structural guarantee on pool shell,Maintenance|Optional pool maintenance & cleaning contracts',
                'faq_data': 'How long does pool construction take?|Most pools are completed within 4–10 weeks from design approval, depending on size, complexity, and weather conditions.,Can you heat the pool for year-round use?|Yes. We install efficient heating systems (solar, heat pump, or gas) that keep your pool comfortable even during Dubai\'s cooler months.,What maintenance does a pool require?|Regular maintenance includes cleaning, chemical balancing, filter maintenance, and equipment checks. We offer maintenance contracts to keep your pool pristine.,Do you handle approvals?|Yes. We manage all necessary approvals from Dubai Municipality and coordinate with your developer if required.,What pool finishes do you offer?|We offer premium tiles, natural stone, pebble finishes, and glass mosaics. We help you choose the perfect finish for your design vision.,Can you integrate water features?|Absolutely. We design and install waterfalls, cascades, fountains, and water walls that integrate seamlessly with your pool.',
                'testimonial_text': 'Our infinity pool overlooking Palm Jumeirah is absolutely stunning. Gold Leaf Scapes managed every detail from design to final handover. The smart heating system means we use it year-round.',
                'testimonial_author': 'Sarah Al Maktoum',
                'testimonial_role': 'Villa Owner – Palm Jumeirah, Dubai',
                'related_services': 'villa-landscaping,pergolas-pavilions,garden-maintenance',
                'featured': True,
                'order': 3,
            },

            # ==========================================================
            # 4️⃣ INTERIOR GREENING
            # ==========================================================
            {
                'title': 'Interior<br><em>Greening</em>',
                'slug': 'interior-greening',
                'short_description': 'Living walls, biophilic installations, interior planting design, and preserved moss art that bring the serenity of nature inside your space.',
                'full_description': 'Biophilic design and interior landscaping services.',
                'icon': 'fa-couch',
                'hero_tag': 'Interior Landscaping',
                'hero_meta_projects': '95+',
                'hero_meta_satisfaction': '4.8 ★',
                'hero_meta_guarantee': '1 Yr',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '95+|Interior Projects|Offices, Hotels & Villas,2–4|Weeks Installation|Design to completion,100%|Custom Designed|Tailored to your space,1yr|Plant Guarantee|All living installations',
                'overview_content': """Biophilic design — bringing nature indoors — transforms spaces, improves wellbeing, and creates memorable brand experiences. Gold Leaf Scapes specializes in interior landscaping that makes powerful visual and emotional impacts.

Our interior greening services include:
• Living green walls (hydroponic and soil-based)
• Vertical gardens for offices and lobbies
• Preserved moss art installations
• Indoor plant styling and arrangements
• Maintenance programs for interior plants

Research shows that indoor plants improve air quality, reduce stress, boost productivity, and enhance brand perception. Whether you're designing a corporate headquarters, hotel lobby, or luxury villa interior, our installations create environments that inspire and impress.

We handle everything from design and plant selection to installation and ongoing care — ensuring your interior landscape thrives for years to come.""",
                'whats_included': """Site assessment & design consultation
Living wall system design
Plant selection & sourcing
Installation & establishment
Irrigation system (for living walls)
LED grow lighting (if needed)
Preserved moss art installation
Maintenance program setup
1-year plant guarantee
Care guide & training""",
                'timeline_data': 'Week 1|Site assessment & design development,Week 2|Plant sourcing & system preparation,Week 3|Installation & establishment,Week 4|Final adjustments & handover',
                'process_steps_data': 'fa-search|Site Assessment|We evaluate light levels, humidity, temperature, and space constraints to design an interior landscape that thrives in your environment.,fa-palette|Design & Plant Selection|Our designers select plants suited to indoor conditions and create layouts that enhance your space\'s aesthetic and function.,fa-tools|System Installation|Living walls, planters, and moss art are installed by our specialized team with attention to detail and minimal disruption.,fa-seedling|Establishment & Care|We establish plants, program irrigation systems, and provide initial care to ensure successful establishment.,fa-book|Handover & Training|Comprehensive care guides and training sessions ensure your team can maintain the installation, or we provide ongoing maintenance services.,fa-sync|Ongoing Maintenance|Optional maintenance contracts keep your interior landscape healthy, vibrant, and impressive year-round.',
                'showcase_projects_data': 'DIFC Office|Living Wall Lobby|large,Hotel Lobby|Moss Art Feature|small,Corporate HQ|Vertical Garden|half,Villa Interior|Plant Styling|half',
                'specs_data': 'Installation Types|Living walls, vertical gardens, moss art, planters,Light Requirements|Low-light to bright indirect light options,Plant Selection|Air-purifying, low-maintenance, climate-adapted species,Irrigation|Automated drip systems for living walls,Lighting|LED grow lights available for low-light areas,Guarantee|1-year guarantee on all living plants,Maintenance|Monthly, bi-monthly, or quarterly maintenance contracts',
                'faq_data': 'Do indoor plants require a lot of maintenance?|Our interior landscapes are designed for low maintenance. We select hardy, air-purifying plants and provide automated irrigation for living walls. Maintenance contracts are available.,Will plants survive in low-light offices?|Yes. We design installations for various light conditions, including low-light areas. LED grow lights can be integrated if needed.,How long do living walls last?|With proper care, living walls can last many years. We provide maintenance programs and replace plants as needed under our guarantee.,What is preserved moss art?|Preserved moss art uses real moss that has been treated to maintain its natural appearance without requiring water or maintenance. It\'s perfect for low-light areas.,Can you work around business hours?|Yes. We schedule installations to minimize disruption. Many installations can be completed during evenings or weekends.,Do you provide maintenance?|Yes. We offer flexible maintenance contracts to keep your interior landscape healthy and vibrant. Our team handles pruning, watering, and plant replacement.',
                'testimonial_text': 'The living wall in our office reception changed the entire atmosphere. Clients constantly comment on it, and our team feels more energized. Gold Leaf Scapes made the process seamless.',
                'testimonial_author': 'Layla Hassan',
                'testimonial_role': 'Head of Operations, Business Bay',
                'related_services': 'villa-landscaping,commercial-landscapes,garden-maintenance',
                'featured': True,
                'order': 4,
            },

            # ==========================================================
            # 5️⃣ PERGOLAS & PAVILIONS
            # ==========================================================
            {
                'title': 'Pergolas &<br><em>Pavilions</em>',
                'slug': 'pergolas-pavilions',
                'short_description': 'Bespoke outdoor structures — from intimate timber pergolas to grand architectural pavilions — designed to extend your living space beautifully.',
                'full_description': 'Custom pergolas, pavilions, and outdoor structures.',
                'icon': 'fa-archway',
                'hero_tag': 'Outdoor Structures',
                'hero_meta_projects': '110+',
                'hero_meta_satisfaction': '4.9 ★',
                'hero_meta_guarantee': '3 Yrs',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '110+|Structures Built|Pergolas & Pavilions,3–6|Weeks Build Time|Design to completion,100%|Custom Designed|Every structure is unique,3yr|Structural Guarantee|Materials & workmanship',
                'overview_content': """Outdoor structures transform gardens into functional, luxurious extensions of your home. Gold Leaf Scapes designs and builds custom pergolas, pavilions, and shade structures that blend architectural elegance with practical function.

Our outdoor structures include:
• Timber pergolas (teak, cedar, or composite)
• Aluminum pergolas with automated louvered roofs
• Garden pavilions and gazebos
• Outdoor kitchens and BBQ stations
• Shade sails and tensile structures
• Integrated lighting and ceiling fans

Every structure is engineered to withstand Dubai's heat, humidity, and occasional storms. We work with premium materials and finishes that age beautifully and require minimal maintenance.

Whether you need a shaded dining area, an outdoor kitchen, or a grand pavilion for entertaining, we create structures that become the heart of your outdoor living space.""",
                'whats_included': """Design consultation & 3D visualization
Structural engineering & approvals
Material selection & sourcing
Foundation & structural installation
Roofing system (fixed or automated)
Integrated lighting design
Ceiling fan installation (optional)
Final finishing & handover
3-year structural guarantee
Maintenance guide""",
                'timeline_data': 'Week 1|Design consultation & material selection,Week 2|Engineering, approvals & fabrication,Week 3–4|Foundation & structural installation,Week 5|Roofing, lighting & finishing,Week 6|Final inspection & handover',
                'process_steps_data': 'fa-drafting-compass|Design & Planning|We design your structure to complement your landscape, optimize shade, and create the perfect outdoor room for your lifestyle.,fa-calculator|Engineering & Approvals|Structural engineering ensures your pergola or pavilion meets all safety standards and municipal requirements.,fa-hammer|Material Selection|We source premium materials — from sustainable teak to low-maintenance aluminum — that suit your design and budget.,fa-tools|Fabrication & Installation|Our skilled craftsmen fabricate and install your structure with precision, ensuring perfect fit and finish.,fa-lightbulb|Lighting & Integration|Integrated LED lighting, ceiling fans, and other features are installed to enhance comfort and ambiance.,fa-key|Handover & Care|Comprehensive handover includes care instructions, warranty documentation, and optional maintenance services.',
                'showcase_projects_data': 'Dubai Hills|Timber Pergola Terrace|large,Emirates Hills|Automated Louvered Roof|small,Palm Jumeirah|Garden Pavilion|half,Jumeirah|Outdoor Kitchen|half',
                'specs_data': 'Structure Types|Pergolas, pavilions, gazebos, shade structures,Materials|Timber (teak, cedar), aluminum, composite, steel,Roofing|Fixed, retractable, automated louvered systems,Lighting|Integrated LED systems with smart controls,Size Range|Small intimate pergolas to large pavilions,Guarantee|3-year structural guarantee on materials & workmanship,Maintenance|Low-maintenance materials; optional maintenance contracts',
                'faq_data': 'What materials are best for Dubai climate?|Aluminum and composite materials are excellent for low maintenance. Teak and cedar offer natural beauty but require more care. We help you choose based on your priorities.,Can you install automated louvered roofs?|Yes. We install automated louvered roof systems that open and close with the touch of a button, giving you control over shade and ventilation.,How long do pergolas last?|Premium materials like aluminum and teak can last 20+ years with proper maintenance. We provide care guides and maintenance services to protect your investment.,Do you handle approvals?|Yes. We manage all necessary approvals for outdoor structures, including developer and municipal requirements.,Can you integrate outdoor kitchens?|Absolutely. We design and install outdoor kitchens, BBQ stations, and dining areas that integrate seamlessly with your pergola or pavilion.,What lighting options are available?|We offer integrated LED lighting systems, ceiling fans with lights, and ambient lighting that creates the perfect atmosphere for evening entertaining.',
                'testimonial_text': 'Our automated louvered pergola is the centerpiece of our garden. We use it year-round — open for stargazing, closed for shade. Gold Leaf Scapes delivered exactly what we envisioned.',
                'testimonial_author': 'Mohammed Al Suwaidi',
                'testimonial_role': 'Villa Owner – Emirates Hills, Dubai',
                'related_services': 'villa-landscaping,swimming-pool-design,garden-maintenance',
                'featured': True,
                'order': 5,
            },

            # ==========================================================
            # 6️⃣ GARDEN MAINTENANCE
            # ==========================================================
            {
                'title': 'Garden<br><em>Maintenance</em>',
                'slug': 'garden-maintenance',
                'short_description': 'Year-round care programmes keeping your landscape in peak condition — including seasonal planting, irrigation management, and expert arboriculture.',
                'full_description': 'Professional landscape maintenance and garden care services.',
                'icon': 'fa-tools',
                'hero_tag': 'Landscape Maintenance',
                'hero_meta_projects': '200+',
                'hero_meta_satisfaction': '4.9 ★',
                'hero_meta_guarantee': 'Ongoing',
                'cta_text': 'Get Free Quote',
                'cta_link': '#',
                'stats_strip_data': '200+|Properties Maintained|Villas & Commercial,Weekly|Service Frequency|Flexible schedules,100%|Expert Care|Trained horticulturists,Ongoing|Service Guarantee|Satisfaction guaranteed',
                'overview_content': """A luxury landscape requires expert care to remain pristine. Gold Leaf Scapes provides comprehensive maintenance services that protect your investment and keep your garden in peak condition year-round.

Our maintenance programs include:
• Scheduled pruning and trimming
• Fertilization and soil health programs
• Irrigation system inspection and adjustment
• Seasonal planting and color rotation
• Pest and disease management
• Palm tree care and arboriculture
• Lawn care and edging
• General garden tidying

We offer flexible maintenance contracts tailored to your needs:
• Monthly visits for comprehensive care
• Bi-monthly for standard maintenance
• Quarterly for low-maintenance landscapes
• One-time services for specific needs

Our team of trained horticulturists understands Dubai's climate and plant requirements. We keep your landscape healthy, vibrant, and impressive — so you can enjoy it without the work.""",
                'whats_included': """Pruning & trimming (trees, shrubs, hedges)
Fertilization & soil amendments
Irrigation system checks & adjustments
Seasonal planting & color rotation
Pest & disease control
Palm tree care & arboriculture
Lawn mowing & edging
Weed control
Garden tidying & debris removal
Monthly service reports""",
                'timeline_data': 'Ongoing|Monthly, bi-monthly, or quarterly visits,Seasonal|Spring & autumn deep-clean services,As Needed|Emergency call-out services available,Annual|Comprehensive landscape health assessment',
                'process_steps_data': 'fa-clipboard-check|Initial Assessment|We assess your landscape\'s current condition, identify needs, and create a customized maintenance plan for your property.,fa-calendar-alt|Scheduled Visits|Regular visits on your preferred schedule ensure consistent care and early detection of any issues.,fa-cut|Pruning & Trimming|Expert pruning maintains plant health, shape, and encourages healthy growth throughout the year.,fa-flask|Fertilization & Health|Seasonal fertilization and soil treatments keep plants healthy and vibrant in Dubai\'s challenging climate.,fa-bug|Pest Management|Early detection and treatment of pests and diseases prevents damage and maintains plant health.,fa-file-alt|Service Reports|Detailed reports after each visit keep you informed about your landscape\'s condition and any recommendations.',
                'showcase_projects_data': 'Villa Portfolio|Maintained Gardens|large,Commercial|Corporate Landscapes|small,Hotel|Resort Grounds|half,Retail|Shopping Center|half',
                'specs_data': 'Service Frequency|Monthly, bi-monthly, quarterly, or one-time,Team Size|2–4 trained horticulturists per visit,Equipment|Professional-grade tools and equipment,Response Time|24–48 hours for urgent issues,Reporting|Detailed service reports after each visit,Guarantee|Satisfaction guaranteed or we make it right',
                'faq_data': 'How often should I have maintenance?|Most luxury landscapes benefit from monthly maintenance. We can adjust frequency based on your landscape\'s needs and your budget.,What happens if a plant dies?|If a plant fails under our care program, we replace it at no charge. We also provide guidance on plant selection for long-term success.,Do you work during summer?|Yes. Our team is experienced working in Dubai\'s summer heat. We adjust schedules and techniques to ensure quality care year-round.,Can you maintain irrigation systems?|Absolutely. We inspect, adjust, and repair irrigation systems as part of our maintenance program to ensure efficient water use.,What areas do you cover?|We provide maintenance services across Dubai, Abu Dhabi, and Sharjah — from Palm Jumeirah to Dubai Hills and everywhere in between.,Do you offer one-time services?|Yes. We provide one-time services for specific needs like deep pruning, seasonal planting, or emergency tree care.',
                'testimonial_text': 'Gold Leaf Scapes has maintained our garden for two years. It looks better now than when it was first installed. Their team is professional, reliable, and truly cares about our landscape.',
                'testimonial_author': 'Fatima Al Mansoori',
                'testimonial_role': 'Villa Owner – Dubai Hills Estate',
                'related_services': 'villa-landscaping,commercial-landscapes,interior-greening',
                'featured': True,
                'order': 6,
            },
        ]

        for service_data in services_data:
            service, created = Service.objects.update_or_create(
                slug=service_data['slug'],
                defaults=service_data
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created service: {service.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Updated service: {service.title}'))

        # Seed process steps
        self.stdout.write('\nSeeding process steps...')
        
        process_steps_data = [
            {
                'icon': 'fa-comments',
                'title': 'Consultation',
                'description': 'On-site meeting to understand your vision, lifestyle and budget. No cookie-cutter solutions.',
                'order': 1,
                'active': True,
            },
            {
                'icon': 'fa-pen-nib',
                'title': 'Concept Design',
                'description': 'Mood boards, planting schemes and initial layouts shaped around your unique brief.',
                'order': 2,
                'active': True,
            },
            {
                'icon': 'fa-cube',
                'title': '3D Visualization',
                'description': 'Photorealistic renders and walkthroughs so you experience the space before build begins.',
                'order': 3,
                'active': True,
            },
            {
                'icon': 'fa-hard-hat',
                'title': 'Expert Build',
                'description': 'Our skilled crews execute every element with precision — on time and on budget.',
                'order': 4,
                'active': True,
            },
            {
                'icon': 'fa-check-circle',
                'title': 'Handover & Care',
                'description': 'Full handover with care guide, warranty, and optional ongoing maintenance plans.',
                'order': 5,
                'active': True,
            },
        ]
        
        for step_data in process_steps_data:
            step, created = ProcessStep.objects.update_or_create(
                title=step_data['title'],
                defaults=step_data
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created process step: {step.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'✓ Updated process step: {step.title}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Gold Leaf Scapes services and process steps seeded successfully!'))
