"""
Context processors for global template variables
"""
from .models import Service


def footer_services(request):
    """
    Make services available to all templates for footer navigation
    """
    services = Service.objects.filter(featured=True).order_by('order', 'title')[:6]
    if not services.exists():
        # Fallback to all services if no featured services
        services = Service.objects.all().order_by('order', 'title')[:6]
    
    return {
        'footer_services': services,
    }

