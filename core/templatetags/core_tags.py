from django import template
from core.models import Teacher, Student, Notification

register = template.Library()

@register.simple_tag
def is_teacher(user):
    """
    Check if a user is a teacher.
    Returns True if user has a Teacher profile, False otherwise.
    """
    if not user or not user.is_authenticated:
        return False
    return Teacher.objects.filter(user=user).exists()

@register.simple_tag
def is_student(user):
    """
    Check if a user is a student.
    Returns True if user has a Student profile, False otherwise.
    """
    if not user or not user.is_authenticated:
        return False
    return Student.objects.filter(user=user).exists()

@register.simple_tag
def unread_notification_count(user):
    """
    Get count of unread notifications for a user.
    """
    if not user or not user.is_authenticated:
        return 0
    return Notification.objects.filter(user=user, is_read=False).count()

