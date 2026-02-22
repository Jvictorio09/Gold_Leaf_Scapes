"""
Role-based access control decorators for dashboard views.
"""
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def blog_author_required(view_func):
    """Decorator: Blog authors and admins can access"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard_login')
        
        # Check if user is admin or blog author
        if hasattr(request.user, 'profile'):
            if not (request.user.profile.is_admin or request.user.profile.is_blog_author):
                raise PermissionDenied("You don't have permission to access this page.")
        elif not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Decorator: Only admins can access"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard_login')
        
        if hasattr(request.user, 'profile'):
            if not request.user.profile.is_admin:
                raise PermissionDenied("Admin access required")
        elif not request.user.is_superuser:
            raise PermissionDenied("Admin access required")
        
        return view_func(request, *args, **kwargs)
    return wrapper

