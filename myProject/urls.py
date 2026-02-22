from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Public routes
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('projects/', views.projects, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Dashboard authentication
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    
    # Dashboard home
    path('dashboard/', views.dashboard_home, name='dashboard_home'),
    
    # Services management
    path('dashboard/services/', views.dashboard_services_list, name='dashboard_services_list'),
    path('dashboard/services/create/', views.dashboard_service_create, name='dashboard_service_create'),
    path('dashboard/services/<int:pk>/edit/', views.dashboard_service_edit, name='dashboard_service_edit'),
    path('dashboard/services/<int:pk>/delete/', views.dashboard_service_delete, name='dashboard_service_delete'),
    
    # Insights management
    path('dashboard/insights/', views.dashboard_insights_list, name='dashboard_insights_list'),
    path('dashboard/insights/create/', views.dashboard_insight_create, name='dashboard_insight_create'),
    path('dashboard/insights/<int:pk>/edit/', views.dashboard_insight_edit, name='dashboard_insight_edit'),
    path('dashboard/insights/<int:pk>/delete/', views.dashboard_insight_delete, name='dashboard_insight_delete'),
    
    # Heroes management
    path('dashboard/heroes/', views.dashboard_heroes_list, name='dashboard_heroes_list'),
    path('dashboard/heroes/create/', views.dashboard_hero_create, name='dashboard_hero_create'),
    path('dashboard/heroes/<int:pk>/edit/', views.dashboard_hero_edit, name='dashboard_hero_edit'),
    path('dashboard/heroes/<int:pk>/delete/', views.dashboard_hero_delete, name='dashboard_hero_delete'),
    
    # Metadata management
    path('dashboard/metadata/', views.dashboard_metadata_list, name='dashboard_metadata_list'),
    path('dashboard/metadata/create/', views.dashboard_metadata_create, name='dashboard_metadata_create'),
    path('dashboard/metadata/<int:pk>/edit/', views.dashboard_metadata_edit, name='dashboard_metadata_edit'),
    path('dashboard/metadata/<int:pk>/delete/', views.dashboard_metadata_delete, name='dashboard_metadata_delete'),
    
    # Gallery management
    path('dashboard/gallery/', views.dashboard_gallery, name='dashboard_gallery'),
    path('dashboard/gallery/upload/', views.gallery_api_upload, name='gallery_api_upload'),
    path('dashboard/gallery/<int:pk>/delete/', views.gallery_api_delete, name='gallery_api_delete'),
    
    # User management
    path('dashboard/users/', views.dashboard_users_list, name='dashboard_users_list'),
    path('dashboard/users/<int:pk>/edit/', views.dashboard_user_edit, name='dashboard_user_edit'),
]

