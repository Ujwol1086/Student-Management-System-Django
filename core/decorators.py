from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from .models import Teacher, Student

def teacher_required(view_func):
    """Decorator to ensure user is a teacher"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            messages.error(request, 'You must be a teacher to access this page.')
            raise PermissionDenied("You must be a teacher to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    """Decorator to ensure user is a student"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        try:
            Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            messages.error(request, 'You must be a student to access this page.')
            raise PermissionDenied("You must be a student to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_or_teacher_required(view_func):
    """Decorator to ensure user is admin or teacher"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        is_admin = request.user.is_staff or request.user.is_superuser
        is_teacher = Teacher.objects.filter(user=request.user).exists()
        
        if not (is_admin or is_teacher):
            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied("You must be an admin or teacher to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    """Decorator to ensure user is admin"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login')
        
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You must be an administrator to access this page.')
            raise PermissionDenied("You must be an administrator to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

