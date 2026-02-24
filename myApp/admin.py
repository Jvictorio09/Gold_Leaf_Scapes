from django.contrib import admin
from .models import (
    UserProfile, Service, Insight, Hero, Metadata,
    MediaAsset, MediaAlbum, ProcessStep, Project, IntroSettings
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'featured', 'order', 'created_at']
    list_filter = ['featured', 'created_at']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'published_at', 'created_at']
    list_filter = ['status', 'created_at', 'published_at']
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['page', 'custom_slug', 'title', 'active', 'order', 'created_at']
    list_filter = ['page', 'active', 'created_at']
    search_fields = ['title', 'subtitle']


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ['page', 'custom_slug', 'title', 'created_at']
    list_filter = ['page', 'created_at']
    search_fields = ['title', 'description', 'keywords']


@admin.register(MediaAlbum)
class MediaAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'cld_folder', 'created_at']
    search_fields = ['title', 'description']


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'format', 'width', 'height', 'bytes_size', 'created_at']
    list_filter = ['format', 'album', 'created_at']
    search_fields = ['title', 'public_id', 'tags_csv']
    readonly_fields = ['public_id', 'secure_url', 'web_url', 'thumb_url', 'bytes_size', 'width', 'height', 'format', 'created_at', 'updated_at']


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['title', 'description']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'featured', 'order', 'created_at']
    list_filter = ['featured', 'related_service', 'created_at']
    search_fields = ['title', 'location', 'category', 'short_description']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(IntroSettings)
class IntroSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'use_svg_fallback', 'updated_at']
    fields = ['intro_image_url', 'use_svg_fallback']
    
    def has_add_permission(self, request):
        # Only allow one instance (singleton)
        return not IntroSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
