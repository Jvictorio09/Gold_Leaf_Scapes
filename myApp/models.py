from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class UserProfile(models.Model):
    """Extended user profile with role information"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('blog_author', 'Blog Author'),
        ('user', 'Regular User'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
    
    @property
    def is_blog_author(self):
        return self.role == 'blog_author'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.user.is_superuser


class MediaAlbum(models.Model):
    """Album/collection for organizing media assets"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cld_folder = models.CharField(max_length=255, blank=True, help_text="Cloudinary folder path")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class MediaAsset(models.Model):
    """Stores Cloudinary URLs (never store files on server)"""
    album = models.ForeignKey(MediaAlbum, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    title = models.CharField(max_length=200)
    public_id = models.CharField(max_length=255, blank=True)
    secure_url = models.URLField(blank=True)  # Original URL
    web_url = models.URLField(blank=True)  # Optimized URL (f_auto,q_auto)
    thumb_url = models.URLField(blank=True)  # Thumbnail URL
    bytes_size = models.PositiveIntegerField(default=0)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    format = models.CharField(max_length=10, blank=True)
    tags_csv = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Service(models.Model):
    """Service offerings"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    hero_image_url = models.URLField(blank=True, help_text="Cloudinary URL for hero image")
    
    # Service card fields
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class (e.g., 'fa-tree')")
    
    # Hero section fields
    hero_tag = models.CharField(max_length=100, blank=True, help_text="Tag shown in hero (e.g., 'Outdoor Landscaping')")
    hero_meta_projects = models.CharField(max_length=50, blank=True, help_text="Projects stat (e.g., '140+')")
    hero_meta_satisfaction = models.CharField(max_length=50, blank=True, help_text="Satisfaction stat (e.g., '4.9 ★')")
    hero_meta_guarantee = models.CharField(max_length=50, blank=True, help_text="Guarantee stat (e.g., '2 Yrs')")
    cta_text = models.CharField(max_length=100, blank=True, help_text="Hero CTA button text")
    cta_link = models.CharField(max_length=255, blank=True, help_text="Hero CTA button link")
    
    # Stats strip (format: "number|label|subtext,number|label|subtext,...")
    stats_strip_data = models.TextField(blank=True, help_text="Stats in format: '140+|Villas Transformed|Across Dubai...,3–8|Weeks to Completion|Depending on...'")
    
    # Overview section
    overview_content = models.TextField(blank=True, help_text="Overview paragraphs (separate with double newline)")
    whats_included = models.TextField(blank=True, help_text="What's included list items (one per line)")
    timeline_data = models.TextField(blank=True, help_text="Timeline in format: 'Week 1|Task description,Week 2|Task description'")
    
    # Process section (format: "icon|title|description,icon|title|description,...")
    process_steps_data = models.TextField(blank=True, help_text="Process steps in format: 'fa-search|Discovery & Site Analysis|Description...'")
    
    # Showcase projects (format: "tag|name|size,tag|name|size,..." where size is 'large', 'small', or 'half')
    showcase_projects_data = models.TextField(blank=True, help_text="Showcase projects in format: 'Dubai Hills Estate|The Palm Residence Garden|large,...'")
    
    # Specs (format: "key|value,key|value,...")
    specs_data = models.TextField(blank=True, help_text="Specs in format: 'Minimum Plot|200 sqm...,Design Style|Tropical...'")
    
    # FAQ (format: "question|answer,question|answer,...")
    faq_data = models.TextField(blank=True, help_text="FAQ in format: 'How long does it take?|Most residential...'")
    
    # Testimonial
    testimonial_text = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    testimonial_role = models.CharField(max_length=200, blank=True)
    
    # Related services (comma-separated service IDs or slugs)
    related_services = models.CharField(max_length=500, blank=True, help_text="Comma-separated service slugs for related services")
    
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})
    
    def get_stats_strip(self):
        """Parse stats_strip_data and return list of dicts"""
        if not self.stats_strip_data:
            return []
        stats = []
        for stat in self.stats_strip_data.split(','):
            if '|' in stat:
                parts = stat.split('|', 2)
                if len(parts) == 3:
                    stats.append({'number': parts[0].strip(), 'label': parts[1].strip(), 'subtext': parts[2].strip()})
        return stats
    
    def get_timeline(self):
        """Parse timeline_data and return list of dicts"""
        if not self.timeline_data:
            return []
        timeline = []
        for item in self.timeline_data.split(','):
            if '|' in item:
                week, task = item.split('|', 1)
                timeline.append({'week': week.strip(), 'task': task.strip()})
        return timeline
    
    def get_process_steps(self):
        """Parse process_steps_data and return list of dicts"""
        if not self.process_steps_data:
            return []
        steps = []
        for step in self.process_steps_data.split(','):
            if '|' in step:
                parts = step.split('|', 2)
                if len(parts) == 3:
                    steps.append({'icon': parts[0].strip(), 'title': parts[1].strip(), 'description': parts[2].strip()})
        return steps
    
    def get_showcase_projects(self):
        """Parse showcase_projects_data and return list of dicts"""
        if not self.showcase_projects_data:
            return []
        projects = []
        for project in self.showcase_projects_data.split(','):
            if '|' in project:
                parts = project.split('|')
                # Support both old (tag|name|size) and new (tag|name|size|image_url) formats
                if len(parts) >= 2:
                    tag = parts[0].strip()
                    name = parts[1].strip()
                    size = parts[2].strip() if len(parts) > 2 and parts[2].strip() else 'half'
                    image_url = parts[3].strip() if len(parts) > 3 and parts[3].strip() else ''
                    projects.append({'tag': tag, 'name': name, 'size': size, 'image_url': image_url})
        return projects
    
    def get_specs(self):
        """Parse specs_data and return list of dicts"""
        if not self.specs_data:
            return []
        specs = []
        for spec in self.specs_data.split(','):
            if '|' in spec:
                key, value = spec.split('|', 1)
                specs.append({'key': key.strip(), 'value': value.strip()})
        return specs
    
    def get_faqs(self):
        """Parse faq_data and return list of dicts"""
        if not self.faq_data:
            return []
        faqs = []
        for faq in self.faq_data.split(','):
            if '|' in faq:
                question, answer = faq.split('|', 1)
                faqs.append({'question': question.strip(), 'answer': answer.strip()})
        return faqs
    
    def get_related_services_list(self):
        """Get related services as Service objects"""
        if not self.related_services:
            return Service.objects.none()
        slugs = [s.strip() for s in self.related_services.split(',') if s.strip()]
        return Service.objects.filter(slug__in=slugs).exclude(id=self.id)[:3]
    
    def get_whats_included_list(self):
        """Parse whats_included and return list of items"""
        if not self.whats_included:
            return []
        return [item.strip() for item in self.whats_included.split('\n') if item.strip()]
    
    def get_clean_title(self):
        """Get title without HTML tags for use in tags/labels"""
        import re
        if not self.title:
            return ''
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', self.title)
        return clean.strip()


class Insight(models.Model):
    """Blog posts / Insights"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True, help_text="Short summary for listings")
    content = models.TextField(blank=True)
    featured_image_url = models.URLField(blank=True, help_text="Cloudinary URL for featured image")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='insights')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})
    
    def render_content(self):
        """
        Render Editor.js JSON content to HTML, or return HTML as-is
        """
        if not self.content:
            return ''
        
        import json
        from django.utils.safestring import mark_safe
        from django.utils.html import escape
        
        # Try to parse as JSON
        try:
            data = json.loads(self.content) if isinstance(self.content, str) else self.content
            blocks = data.get('blocks', [])
        except (json.JSONDecodeError, AttributeError, TypeError):
            # If not JSON, assume it's HTML and return as-is
            return mark_safe(self.content)
        
        html_parts = []
        
        for block in blocks:
            block_type = block.get('type')
            block_data = block.get('data', {})
            
            if block_type == 'paragraph':
                text = block_data.get('text', '')
                html_parts.append(f'<p>{text}</p>')
            
            elif block_type == 'header':
                level = block_data.get('level', 2)
                text = block_data.get('text', '')
                html_parts.append(f'<h{level}>{text}</h{level}>')
            
            elif block_type == 'list':
                style = block_data.get('style', 'unordered')
                items = block_data.get('items', [])
                tag = 'ul' if style == 'unordered' else 'ol'
                items_html = ''.join(f'<li>{item}</li>' for item in items)
                html_parts.append(f'<{tag} class="styled">{items_html}</{tag}>')
            
            elif block_type == 'quote':
                text = block_data.get('text', '')
                caption = block_data.get('caption', '')
                html_parts.append(f'<div class="pullquote"><p>{text}</p>')
                if caption:
                    html_parts.append(f'<cite>{escape(caption)}</cite>')
                html_parts.append('</div>')
            
            elif block_type == 'pullquote':
                text = block_data.get('text', '')
                citation = block_data.get('citation', '')
                html_parts.append(f'<div class="pullquote"><p>{text}</p>')
                if citation:
                    html_parts.append(f'<cite>{escape(citation)}</cite>')
                html_parts.append('</div>')
            
            elif block_type == 'statCallout':
                stat1 = block_data.get('stat1', {})
                stat2 = block_data.get('stat2', {})
                stat3 = block_data.get('stat3', {})
                html_parts.append('<div class="stat-callout">')
                for stat in [stat1, stat2, stat3]:
                    num = stat.get('num', '')
                    label = stat.get('label', '')
                    html_parts.append(f'<div class="stat-cell"><div class="num">{escape(num)}</div><div class="lbl">{escape(label)}</div></div>')
                html_parts.append('</div>')
            
            elif block_type == 'imageCaption':
                url = block_data.get('url', '')
                caption = block_data.get('caption', '')
                style = block_data.get('style', 'teal')
                if url:
                    html_parts.append('<div class="article-img">')
                    html_parts.append(f'<div class="article-img-inner {escape(style)}">')
                    html_parts.append(f'<img src="{escape(url)}" alt="{escape(caption)}" style="width:100%;height:100%;object-fit:cover;">')
                    html_parts.append('</div>')
                    html_parts.append('</div>')
                    if caption:
                        html_parts.append(f'<p class="img-caption">{escape(caption)}</p>')
            
            elif block_type == 'image':
                url = block_data.get('url', '')
                caption = block_data.get('caption', '')
                if url:
                    html_parts.append('<div class="article-img">')
                    html_parts.append('<div class="article-img-inner teal">')
                    html_parts.append(f'<img src="{escape(url)}" alt="{escape(caption)}" style="width:100%;height:100%;object-fit:cover;">')
                    html_parts.append('</div>')
                    html_parts.append('</div>')
                    if caption:
                        html_parts.append(f'<p class="img-caption">{escape(caption)}</p>')
            
            elif block_type == 'code':
                code = block_data.get('code', '')
                html_parts.append(f'<pre><code>{escape(code)}</code></pre>')
            
            elif block_type == 'delimiter':
                html_parts.append('<hr class="ce-delimiter">')
            
            elif block_type == 'linkTool':
                link = block_data.get('link', '')
                meta = block_data.get('meta', {})
                title = meta.get('title', link)
                html_parts.append(f'<p><a href="{escape(link)}">{escape(title)}</a></p>')
        
        return mark_safe(''.join(html_parts))


class Hero(models.Model):
    """Page hero sections"""
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('services', 'Services'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('custom', 'Custom'),
    ]
    
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, default='home')
    custom_slug = models.SlugField(blank=True, help_text="For custom pages")
    eyebrow = models.CharField(max_length=200, blank=True, help_text="Small text above title (e.g., 'Dubai's Premier...')")
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    background_image_url = models.URLField(blank=True, help_text="Cloudinary URL for background")
    cta_text = models.CharField(max_length=100, blank=True, help_text="Primary CTA button text")
    cta_link = models.CharField(max_length=255, blank=True, help_text="Primary CTA button link")
    secondary_cta_text = models.CharField(max_length=100, blank=True, help_text="Secondary CTA button text")
    secondary_cta_link = models.CharField(max_length=255, blank=True, help_text="Secondary CTA button link")
    # Stats fields (JSON stored as text, format: "stat1_number|stat1_label,stat2_number|stat2_label,stat3_number|stat3_label")
    stats_data = models.CharField(max_length=500, blank=True, help_text="Stats in format: '3+|Years in Dubai,340+|Projects Completed,98%|Client Satisfaction'")
    active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['page', 'order']
        unique_together = [['page', 'custom_slug']]
    
    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"
    
    def get_stats(self):
        """Parse stats_data and return list of dicts with 'number' and 'label' keys"""
        if not self.stats_data:
            return []
        stats = []
        for stat in self.stats_data.split(','):
            if '|' in stat:
                number, label = stat.split('|', 1)
                stats.append({'number': number.strip(), 'label': label.strip()})
        return stats


class Metadata(models.Model):
    """SEO metadata for pages"""
    PAGE_CHOICES = [
        ('home', 'Home'),
        ('services', 'Services'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('blog', 'Blog'),
        ('custom', 'Custom'),
    ]
    
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, default='home')
    custom_slug = models.SlugField(blank=True, help_text="For custom pages")
    title = models.CharField(max_length=200, help_text="SEO title (meta title)")
    description = models.TextField(blank=True, help_text="SEO description (meta description)")
    keywords = models.CharField(max_length=500, blank=True, help_text="Comma-separated keywords")
    og_image_url = models.URLField(blank=True, help_text="Open Graph image URL (Cloudinary)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['page', 'custom_slug']
        unique_together = [['page', 'custom_slug']]
    
    def __str__(self):
        return f"{self.get_page_display()} - {self.title}"


class ProcessStep(models.Model):
    """General company process steps (used in services_process.html)"""
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fa-comments')")
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Display order")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title


class Project(models.Model):
    """Portfolio projects"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=200, help_text="Location (e.g., 'Dubai Hills Estate')")
    category = models.CharField(max_length=200, help_text="Category/tags (e.g., 'Villa Landscaping + Pool')")
    
    # Hero/Featured Image
    hero_image_url = models.URLField(blank=True, help_text="Cloudinary URL for hero/featured image")
    
    # Project Details
    short_description = models.TextField(blank=True, help_text="Brief description for cards")
    full_description = models.TextField(blank=True, help_text="Full project description")
    
    # Project Specifications (format: "key|value,key|value,...")
    specs_data = models.TextField(blank=True, help_text="Project specs in format: 'Area|500 sqm,Completion|2024,Style|Tropical Modern'")
    
    # Gallery Images (comma-separated Cloudinary URLs)
    gallery_images = models.TextField(blank=True, help_text="Comma-separated Cloudinary URLs for gallery")
    
    # Related Service (optional)
    related_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='projects')
    
    # Display
    featured = models.BooleanField(default=False, help_text="Show on homepage portfolio section")
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def get_specs(self):
        """Parse specs_data and return list of dicts"""
        if not self.specs_data:
            return []
        specs = []
        for spec in self.specs_data.split(','):
            if '|' in spec:
                parts = spec.split('|')
                if len(parts) == 2:
                    specs.append({'key': parts[0].strip(), 'value': parts[1].strip()})
        return specs
    
    def get_gallery_list(self):
        """Parse gallery_images and return list of URLs"""
        if not self.gallery_images:
            return []
        return [url.strip() for url in self.gallery_images.split(',') if url.strip()]


class IntroSettings(models.Model):
    """Settings for the intro section on the home page (singleton)"""
    intro_image_url = models.URLField(blank=True, help_text="Cloudinary URL for intro section image (replaces SVG)")
    use_svg_fallback = models.BooleanField(default=True, help_text="Use SVG illustration if no image URL is provided")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Intro Settings"
        verbose_name_plural = "Intro Settings"
    
    def __str__(self):
        return "Intro Section Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create the singleton instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj