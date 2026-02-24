from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
import json
import os
import re
import resend

from .models import (
    UserProfile, Service, Insight, Hero, Metadata, 
    MediaAsset, MediaAlbum, ProcessStep, Project, IntroSettings
)
from .decorators import admin_required, blog_author_required
from .utils.cloudinary_utils import (
    smart_compress_to_bytes, upload_to_cloudinary, TARGET_BYTES
)


# ==================== PUBLIC VIEWS ====================

def home(request):
    # Get active hero for home page
    hero = Hero.objects.filter(page='home', active=True).order_by('order').first()
    
    # Get featured services for the services section
    services = Service.objects.filter(featured=True).order_by('order', 'title')
    if not services.exists():
        services = Service.objects.all().order_by('order', 'title')[:6]
    
    # Get featured projects for the portfolio section
    projects = Project.objects.filter(featured=True).order_by('order', '-created_at')[:4]
    
    # Get intro settings
    intro_settings = IntroSettings.get_settings()
    
    context = {
        'hero': hero,
        'services': services,
        'projects': projects,
        'intro_settings': intro_settings,
    }
    return render(request, 'index.html', context)

def services(request):
    # Get hero for services page
    hero = Hero.objects.filter(page='services', active=True).order_by('order').first()

    services_list = Service.objects.filter(featured=True).order_by('order', 'title')
    if not services_list.exists():
        services_list = Service.objects.all().order_by('order', 'title')
    
    # Get process steps for the process section
    process_steps = ProcessStep.objects.filter(active=True).order_by('order')
    
    return render(request, 'services.html', {
        'hero': hero,
        'services': services_list,
        'process_steps': process_steps,
    })

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    # Use other services (with hero images) to power the showcase tiles
    showcase_services = Service.objects.filter(featured=True).exclude(id=service.id).order_by('order', 'title')[:4]
    return render(request, 'service_detail.html', {
        'service': service,
        'showcase_services': showcase_services,
    })

def projects(request):
    """Projects catalog page"""
    projects_list = Project.objects.all().order_by('-featured', 'order', '-created_at')
    
    # Get unique categories for filtering
    categories = Project.objects.exclude(category='').values_list('category', flat=True).distinct()
    
    return render(request, 'projects.html', {
        'projects': projects_list,
        'categories': categories,
    })

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    
    # Get related projects (same category or featured)
    related_projects = Project.objects.exclude(id=project.id).filter(featured=True).order_by('?')[:3]
    if related_projects.count() < 3:
        # Fill with any other projects
        additional = Project.objects.exclude(id=project.id).exclude(id__in=[p.id for p in related_projects]).order_by('?')[:3-related_projects.count()]
        related_projects = list(related_projects) + list(additional)
    
    return render(request, 'project_detail.html', {
        'project': project,
        'related_projects': related_projects,
    })

def blog_overview(request):
    """Blog overview page - list of all published insights"""
    insights = Insight.objects.filter(status='published').order_by('-published_at', '-created_at')
    
    # Pagination
    paginator = Paginator(insights, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog_page/blog_overview.html', {
        'insights': page_obj,
        'page_obj': page_obj,
    })

def blog_detail(request, slug):
    """Blog detail page - single insight/article"""
    insight = get_object_or_404(Insight, slug=slug, status='published')
    
    # Get related insights (same author or recent)
    related_insights = Insight.objects.exclude(id=insight.id).filter(
        status='published'
    ).order_by('-published_at', '-created_at')[:3]
    
    return render(request, 'blog_page/blog_detail.html', {
        'insight': insight,
        'related_insights': related_insights,
    })


# ==================== AUTHENTICATION ====================

def dashboard_login(request):
    """Login view for dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/login.html', {'form': form})


@login_required
def dashboard_logout(request):
    """Logout view"""
    logout(request)
    return redirect('dashboard_login')


# ==================== DASHBOARD HOME ====================

@login_required
def dashboard_home(request):
    """Dashboard home page - overview"""
    # Redirect Blog Authors directly to insights since they can't access other sections
    if hasattr(request.user, 'profile') and request.user.profile.is_blog_author and not request.user.profile.is_admin:
        return redirect('dashboard_insights_list')
    
    context = {
        'services_count': Service.objects.count(),
        'insights_count': Insight.objects.count(),
        'heroes_count': Hero.objects.count(),
        'media_count': MediaAsset.objects.count(),
        'recent_insights': Insight.objects.filter(status='published')[:5],
        'recent_services': Service.objects.all()[:5],
    }
    return render(request, 'dashboard/home.html', context)


# ==================== SERVICES MANAGEMENT ====================

@login_required
@admin_required
def dashboard_services_list(request):
    """List all services"""
    services = Service.objects.all()
    return render(request, 'dashboard/services/list.html', {'services': services})


@login_required
@admin_required
def dashboard_service_create(request):
    """Create new service"""
    if request.method == 'POST':
        title = request.POST.get('title')
        short_description = request.POST.get('short_description', '')
        full_description = request.POST.get('full_description', '')
        hero_image_url = request.POST.get('hero_image_url', '')
        featured = request.POST.get('featured') == 'on'
        order = int(request.POST.get('order', 0))
        
        service = Service.objects.create(
            title=title,
            short_description=short_description,
            full_description=full_description,
            hero_image_url=hero_image_url,
            featured=featured,
            order=order
        )
        return redirect('dashboard_services_list')
    
    return render(request, 'dashboard/services/create.html')


@login_required
@admin_required
def dashboard_service_edit(request, pk):
    """Edit existing service"""
    service = get_object_or_404(Service, pk=pk)
    
    if request.method == 'POST':
        service.title = request.POST.get('title')
        service.short_description = request.POST.get('short_description', '')
        service.full_description = request.POST.get('full_description', '')
        service.hero_image_url = request.POST.get('hero_image_url', '')
        service.featured = request.POST.get('featured') == 'on'
        service.order = int(request.POST.get('order', 0))
        service.save()
        return redirect('dashboard_services_list')
    
    return render(request, 'dashboard/services/edit.html', {'service': service})


@login_required
@admin_required
@require_POST
def dashboard_service_delete(request, pk):
    """Delete service"""
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('dashboard_services_list')


# ==================== INSIGHTS MANAGEMENT ====================

@login_required
@blog_author_required
def dashboard_insights_list(request):
    """List all insights"""
    insights = Insight.objects.all()
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        insights = insights.filter(status=status_filter)
    
    # Filter by author if not admin
    if hasattr(request.user, 'profile') and not request.user.profile.is_admin:
        insights = insights.filter(author=request.user)
    
    # Calculate stats
    from django.utils import timezone
    from datetime import datetime
    total_count = insights.count()
    published_count = insights.filter(status='published').count()
    draft_count = insights.filter(status='draft').count()
    
    # Count posts from current month
    now = timezone.now()
    this_month_count = insights.filter(created_at__year=now.year, created_at__month=now.month).count()
    
    context = {
        'insights': insights,
        'total_count': total_count,
        'published_count': published_count,
        'draft_count': draft_count,
        'this_month_count': this_month_count,
    }
    
    return render(request, 'dashboard/insights/list.html', context)


@login_required
@blog_author_required
def dashboard_insight_create(request):
    """Create new insight"""
    if request.method == 'POST':
        title = request.POST.get('title')
        excerpt = request.POST.get('excerpt', '')
        content = request.POST.get('content', '')  # Editor.js JSON
        featured_image_url = request.POST.get('featured_image_url', '')
        status = request.POST.get('status', 'draft')
        slug = request.POST.get('slug', '').strip()
        
        # Content can be HTML (from Quill) or JSON (from Editor.js)
        # Both are acceptable, so we keep the content as-is
        
        insight = Insight.objects.create(
            title=title,
            excerpt=excerpt,
            content=content,
            featured_image_url=featured_image_url,
            status=status,
            author=request.user
        )
        
        # Set slug if provided
        if slug:
            insight.slug = slug
            insight.save()
        
        # Set published_at if publishing
        if status == 'published' and not insight.published_at:
            from django.utils import timezone
            insight.published_at = timezone.now()
            insight.save()
        
        return redirect('dashboard_insights_list')
    
    return render(request, 'dashboard/insights/create.html')


@login_required
@blog_author_required
def dashboard_insight_edit(request, pk):
    """Edit existing insight"""
    insight = get_object_or_404(Insight, pk=pk)
    
    # Check permission (author or admin)
    if hasattr(request.user, 'profile') and not request.user.profile.is_admin:
        if insight.author != request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You can only edit your own insights.")
    
    if request.method == 'POST':
        insight.title = request.POST.get('title')
        insight.excerpt = request.POST.get('excerpt', '')
        content = request.POST.get('content', '')  # Editor.js JSON
        
        # Content can be HTML (from Quill) or JSON (from Editor.js)
        # Both are acceptable, so we update the content
        if content:
            insight.content = content
        
        insight.featured_image_url = request.POST.get('featured_image_url', '')
        status = request.POST.get('status', 'draft')
        slug = request.POST.get('slug', '').strip()
        
        # Update slug if provided
        if slug:
            insight.slug = slug
        
        # Handle status change
        old_status = insight.status
        insight.status = status
        
        # Set published_at if publishing for the first time
        if status == 'published' and old_status != 'published' and not insight.published_at:
            from django.utils import timezone
            insight.published_at = timezone.now()
        
        insight.save()
        return redirect('dashboard_insights_list')
    
    return render(request, 'dashboard/insights/edit.html', {'insight': insight})


@login_required
@blog_author_required
@require_POST
def dashboard_insight_delete(request, pk):
    """Delete insight"""
    insight = get_object_or_404(Insight, pk=pk)
    
    # Check permission
    if hasattr(request.user, 'profile') and not request.user.profile.is_admin:
        if insight.author != request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("You can only delete your own insights.")
    
    insight.delete()
    return redirect('dashboard_insights_list')


# ==================== HEROES MANAGEMENT ====================

@login_required
@admin_required
def dashboard_heroes_list(request):
    """List all heroes"""
    heroes = Hero.objects.all()
    return render(request, 'dashboard/heroes/list.html', {'heroes': heroes})


@login_required
@admin_required
def dashboard_hero_create(request):
    """Create new hero"""
    if request.method == 'POST':
        page = request.POST.get('page')
        custom_slug = request.POST.get('custom_slug', '')
        eyebrow = request.POST.get('eyebrow', '')
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle', '')
        background_image_url = request.POST.get('background_image_url', '')
        cta_text = request.POST.get('cta_text', '')
        cta_link = request.POST.get('cta_link', '')
        secondary_cta_text = request.POST.get('secondary_cta_text', '')
        secondary_cta_link = request.POST.get('secondary_cta_link', '')
        stats_data = request.POST.get('stats_data', '')
        active = request.POST.get('active') == 'on'
        order = int(request.POST.get('order', 0))
        
        hero = Hero.objects.create(
            page=page,
            custom_slug=custom_slug,
            eyebrow=eyebrow,
            title=title,
            subtitle=subtitle,
            background_image_url=background_image_url,
            cta_text=cta_text,
            cta_link=cta_link,
            secondary_cta_text=secondary_cta_text,
            secondary_cta_link=secondary_cta_link,
            stats_data=stats_data,
            active=active,
            order=order
        )
        return redirect('dashboard_heroes_list')
    
    return render(request, 'dashboard/heroes/create.html')


@login_required
@admin_required
def dashboard_hero_edit(request, pk):
    """Edit existing hero"""
    hero = get_object_or_404(Hero, pk=pk)
    
    if request.method == 'POST':
        hero.page = request.POST.get('page')
        hero.custom_slug = request.POST.get('custom_slug', '')
        hero.eyebrow = request.POST.get('eyebrow', '')
        hero.title = request.POST.get('title')
        hero.subtitle = request.POST.get('subtitle', '')
        hero.background_image_url = request.POST.get('background_image_url', '')
        hero.cta_text = request.POST.get('cta_text', '')
        hero.cta_link = request.POST.get('cta_link', '')
        hero.secondary_cta_text = request.POST.get('secondary_cta_text', '')
        hero.secondary_cta_link = request.POST.get('secondary_cta_link', '')
        hero.stats_data = request.POST.get('stats_data', '')
        hero.active = request.POST.get('active') == 'on'
        hero.order = int(request.POST.get('order', 0))
        hero.save()
        return redirect('dashboard_heroes_list')
    
    return render(request, 'dashboard/heroes/edit.html', {'hero': hero})


@login_required
@admin_required
@require_POST
def dashboard_hero_delete(request, pk):
    """Delete hero"""
    hero = get_object_or_404(Hero, pk=pk)
    hero.delete()
    return redirect('dashboard_heroes_list')


# ==================== PROJECTS MANAGEMENT ====================

@login_required
@admin_required
def dashboard_projects_list(request):
    """List all projects"""
    projects = Project.objects.all().order_by('-featured', 'order', '-created_at')
    return render(request, 'dashboard/projects/list.html', {'projects': projects})


@login_required
@admin_required
def dashboard_project_create(request):
    """Create new project"""
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location', '')
        category = request.POST.get('category', '')
        hero_image_url = request.POST.get('hero_image_url', '')
        short_description = request.POST.get('short_description', '')
        full_description = request.POST.get('full_description', '')
        specs_data = request.POST.get('specs_data', '')
        gallery_images = request.POST.get('gallery_images', '')
        related_service_id = request.POST.get('related_service', '')
        featured = request.POST.get('featured') == 'on'
        order = int(request.POST.get('order', 0))
        
        project = Project.objects.create(
            title=title,
            location=location,
            category=category,
            hero_image_url=hero_image_url,
            short_description=short_description,
            full_description=full_description,
            specs_data=specs_data,
            gallery_images=gallery_images,
            related_service_id=related_service_id if related_service_id else None,
            featured=featured,
            order=order
        )
        return redirect('dashboard_projects_list')
    
    services = Service.objects.all().order_by('title')
    return render(request, 'dashboard/projects/create.html', {'services': services})


@login_required
@admin_required
def dashboard_project_edit(request, pk):
    """Edit existing project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.location = request.POST.get('location', '')
        project.category = request.POST.get('category', '')
        project.hero_image_url = request.POST.get('hero_image_url', '')
        project.short_description = request.POST.get('short_description', '')
        project.full_description = request.POST.get('full_description', '')
        project.specs_data = request.POST.get('specs_data', '')
        project.gallery_images = request.POST.get('gallery_images', '')
        related_service_id = request.POST.get('related_service', '')
        project.related_service_id = related_service_id if related_service_id else None
        project.featured = request.POST.get('featured') == 'on'
        project.order = int(request.POST.get('order', 0))
        project.save()
        return redirect('dashboard_projects_list')
    
    services = Service.objects.all().order_by('title')
    return render(request, 'dashboard/projects/edit.html', {'project': project, 'services': services})


@login_required
@admin_required
@require_POST
def dashboard_project_delete(request, pk):
    """Delete project"""
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('dashboard_projects_list')


# ==================== METADATA MANAGEMENT ====================

@login_required
@admin_required
def dashboard_metadata_list(request):
    """List all metadata"""
    metadata_list = Metadata.objects.all()
    return render(request, 'dashboard/metadata/list.html', {'metadata_list': metadata_list})


@login_required
@admin_required
def dashboard_metadata_create(request):
    """Create new metadata"""
    if request.method == 'POST':
        page = request.POST.get('page')
        custom_slug = request.POST.get('custom_slug', '')
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        keywords = request.POST.get('keywords', '')
        og_image_url = request.POST.get('og_image_url', '')
        
        metadata = Metadata.objects.create(
            page=page,
            custom_slug=custom_slug,
            title=title,
            description=description,
            keywords=keywords,
            og_image_url=og_image_url
        )
        return redirect('dashboard_metadata_list')
    
    return render(request, 'dashboard/metadata/create.html')


@login_required
@admin_required
def dashboard_metadata_edit(request, pk):
    """Edit existing metadata"""
    metadata = get_object_or_404(Metadata, pk=pk)
    
    if request.method == 'POST':
        metadata.page = request.POST.get('page')
        metadata.custom_slug = request.POST.get('custom_slug', '')
        metadata.title = request.POST.get('title')
        metadata.description = request.POST.get('description', '')
        metadata.keywords = request.POST.get('keywords', '')
        metadata.og_image_url = request.POST.get('og_image_url', '')
        metadata.save()
        return redirect('dashboard_metadata_list')
    
    return render(request, 'dashboard/metadata/edit.html', {'metadata': metadata})


@login_required
@admin_required
@require_POST
def dashboard_metadata_delete(request, pk):
    """Delete metadata"""
    metadata = get_object_or_404(Metadata, pk=pk)
    metadata.delete()
    return redirect('dashboard_metadata_list')


# ==================== INTRO SETTINGS MANAGEMENT ====================

@login_required
@admin_required
def dashboard_intro_settings(request):
    """Edit intro section settings"""
    intro_settings = IntroSettings.get_settings()
    
    if request.method == 'POST':
        intro_settings.intro_image_url = request.POST.get('intro_image_url', '')
        intro_settings.use_svg_fallback = request.POST.get('use_svg_fallback') == 'on'
        intro_settings.save()
        return redirect('dashboard_intro_settings')
    
    return render(request, 'dashboard/intro_settings/edit.html', {'intro_settings': intro_settings})


# ==================== GALLERY MANAGEMENT ====================

@login_required
@blog_author_required
def dashboard_gallery(request):
    """Gallery page with upload interface"""
    # Get or create default album
    default_album, created = MediaAlbum.objects.get_or_create(
        title='Default',
        defaults={'description': 'Default album for uploads', 'cld_folder': 'uploads'}
    )
    
    assets = MediaAsset.objects.all()
    
    # Pagination
    paginator = Paginator(assets, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/gallery/index.html', {
        'page_obj': page_obj,
        'default_album': default_album
    })


@login_required
@require_POST
def gallery_api_upload(request):
    """API endpoint to upload new images to the gallery"""
    try:
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({'success': False, 'error': 'No files provided'})
        
        # Get or create default album
        default_album, created = MediaAlbum.objects.get_or_create(
            title='Default',
            defaults={'description': 'Default album for uploads', 'cld_folder': 'uploads'}
        )
        
        uploaded_images = []
        
        for file in files:
            try:
                # Always convert to WebP format before upload
                # This ensures optimal performance and consistent format
                file.seek(0)
                file_bytes = smart_compress_to_bytes(file)
                
                # Generate clean public_id from filename (remove extension since it will be WebP)
                base_name = file.name.rsplit('.', 1)[0] if '.' in file.name else file.name
                public_id = slugify(base_name)[:120]
                
                # Upload to Cloudinary (already in WebP format)
                result, web_url, thumb_url = upload_to_cloudinary(
                    file_bytes=file_bytes,
                    folder="uploads",
                    public_id=public_id,
                    tags=None
                )
                
                # Create MediaAsset record
                asset = MediaAsset.objects.create(
                    album=default_album,
                    title=file.name.split('.')[0],
                    public_id=result.get('public_id', ''),
                    secure_url=result.get('secure_url', ''),
                    web_url=web_url,
                    thumb_url=thumb_url,
                    bytes_size=result.get('bytes', 0),
                    width=result.get('width', 0),
                    height=result.get('height', 0),
                    format=result.get('format', ''),
                )
                
                uploaded_images.append({
                    'id': asset.id,
                    'title': asset.title,
                    'secure_url': asset.secure_url,
                    'web_url': asset.web_url,
                    'thumb_url': asset.thumb_url,
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False, 
                    'error': f'Failed to upload {file.name}: {str(e)}'
                })
        
        return JsonResponse({
            'success': True,
            'images': uploaded_images
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@blog_author_required
def gallery_api_list(request):
    """API endpoint to get all gallery images as JSON"""
    try:
        assets = MediaAsset.objects.all().order_by('-created_at')
        
        images = []
        for asset in assets:
            images.append({
                'id': asset.id,
                'title': asset.title,
                'secure_url': asset.secure_url,
                'web_url': asset.web_url,
                'thumb_url': asset.thumb_url,
                'width': asset.width,
                'height': asset.height,
                'format': asset.format,
            })
        
        return JsonResponse({
            'success': True,
            'images': images
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
@require_POST
def gallery_api_delete(request, pk):
    """API endpoint to delete an image"""
    try:
        asset = get_object_or_404(MediaAsset, pk=pk)
        asset.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ==================== USER MANAGEMENT ====================

@login_required
@admin_required
def dashboard_users_list(request):
    """List all users"""
    users = User.objects.all().select_related('profile')
    return render(request, 'dashboard/users/list.html', {'users': users})


@login_required
@admin_required
def dashboard_user_edit(request, pk):
    """Edit user role"""
    user = get_object_or_404(User, pk=pk)
    
    # Get or create profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        role = request.POST.get('role', 'user')
        profile.role = role
        profile.save()
        return redirect('dashboard_users_list')
    
    return render(request, 'dashboard/users/edit.html', {'user': user, 'profile': profile})


# ==================== CONTACT FORM ====================

@require_POST
def contact_form_submit(request):
    """Handle contact form submission with Resend email"""
    try:
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        form_type = request.POST.get('form_type', 'consultation')  # 'consultation' or 'quote'
        
        # Honeypot field (bot protection) - should be empty
        honeypot = request.POST.get('website', '').strip()
        if honeypot:
            # Bot detected
            return JsonResponse({'success': False, 'error': 'Invalid submission'}, status=400)
        
        # Checkbox validation (bot protection)
        terms_accepted = request.POST.get('terms_accepted', '')
        if not terms_accepted:
            return JsonResponse({'success': False, 'error': 'Please accept the terms and conditions'}, status=400)
        
        # Validate required fields
        if not name or not email or not message:
            return JsonResponse({'success': False, 'error': 'Please fill in all required fields'}, status=400)
        
        # Validate email format
        if '@' not in email or '.' not in email.split('@')[1]:
            return JsonResponse({'success': False, 'error': 'Please enter a valid email address'}, status=400)
        
        # Send email using Resend
        if not settings.RESEND_API_KEY:
            return JsonResponse({'success': False, 'error': 'Email service not configured'}, status=500)
        
        # Get email settings with fallbacks
        from_email = settings.RESEND_FROM_EMAIL or os.environ.get('DEFAULT_FROM_EMAIL', '')
        to_email = settings.RESEND_TO_EMAIL or os.environ.get('DEFAULT_FROM_EMAIL', '')
        reply_to_email = os.environ.get('RESEND_REPLY_TO', '')
        
        # Validate email addresses
        if not from_email or not to_email:
            return JsonResponse({'success': False, 'error': 'Email service not properly configured'}, status=500)
        
        # Parse FROM email if it's in "Name <email>" format
        # Resend accepts both formats, but let's extract just the email if needed
        from_match = re.search(r'<([^>]+)>', from_email)
        if from_match:
            from_email = from_match.group(1)
        else:
            # If no angle brackets, use as is (should be just email)
            from_email = from_email.strip()
        
        resend.api_key = settings.RESEND_API_KEY
        
        # Determine subject based on form type
        if form_type == 'quote':
            subject = f"New Quote Request from {name}"
        else:
            subject = f"New Consultation Request from {name}"
        
        # Email body
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #B8922A;">New {form_type.title()} Request</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone if phone else 'Not provided'}</p>
            <p><strong>Message:</strong></p>
            <p style="background: #f5f5f5; padding: 15px; border-left: 3px solid #B8922A; margin: 10px 0;">
                {message.replace(chr(10), '<br>')}
            </p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                This email was sent from the Gold Leaf Scapes website contact form.
            </p>
        </body>
        </html>
        """
        
        # Build email params
        params = {
            "from": str(from_email),
            "to": [str(to_email)],
            "subject": subject,
            "html": email_body,
        }
        
        # Add reply_to if configured, otherwise use sender's email
        if reply_to_email:
            params["reply_to"] = str(reply_to_email)
        else:
            params["reply_to"] = email
        
        try:
            email_response = resend.Emails.send(params)
            # Check if email was sent successfully
            if email_response and hasattr(email_response, 'id'):
                return JsonResponse({
                    'success': True, 
                    'message': 'Thank you! We will get back to you soon.'
                })
            else:
                return JsonResponse({'success': False, 'error': 'Failed to send email'}, status=500)
        except Exception as email_error:
            if settings.DEBUG:
                print(f"Resend API error: {str(email_error)}")
            return JsonResponse({'success': False, 'error': 'Failed to send email. Please try again later.'}, status=500)
            
    except Exception as e:
        # Log error in production
        if settings.DEBUG:
            print(f"Contact form error: {str(e)}")
        return JsonResponse({'success': False, 'error': 'An error occurred. Please try again later.'}, status=500)
