from django.db.models import Q
from django.utils import timezone
from .models import Attendance, AuditLog, Course, Student

def log_attendance_change(action, attendance, user, old_status=None, new_status=None, ip_address=None, notes=''):
    """Helper function to create audit log entries"""
    AuditLog.objects.create(
        attendance=attendance,
        action=action,
        user=user,
        student=attendance.student if attendance else None,
        course=attendance.course if attendance else None,
        date=attendance.date if attendance else None,
        old_status=old_status,
        new_status=new_status,
        ip_address=ip_address,
        notes=notes
    )

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def calculate_attendance_percentage(student, course):
    """Calculate attendance percentage for a student in a course"""
    total_records = Attendance.objects.filter(student=student, course=course).count()
    if total_records == 0:
        return 0.0
    
    present_count = Attendance.objects.filter(student=student, course=course, status=True).count()
    return round((present_count / total_records) * 100, 2)

def get_course_attendance_stats(course):
    """Get attendance statistics for a course"""
    total_classes = Attendance.objects.filter(course=course).values('date').distinct().count()
    total_records = Attendance.objects.filter(course=course).count()
    present_count = Attendance.objects.filter(course=course, status=True).count()
    absent_count = Attendance.objects.filter(course=course, status=False).count()
    
    enrolled_students = course.students.count()
    avg_attendance = 0.0
    if total_records > 0:
        avg_attendance = round((present_count / total_records) * 100, 2)
    
    return {
        'total_classes': total_classes,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'enrolled_students': enrolled_students,
        'average_attendance': avg_attendance,
    }

def filter_attendance(queryset, course_id=None, student_id=None, date_from=None, date_to=None, status=None):
    """Filter attendance queryset based on parameters"""
    if course_id:
        queryset = queryset.filter(course_id=course_id)
    if student_id:
        queryset = queryset.filter(student_id=student_id)
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    if status is not None:
        queryset = queryset.filter(status=status)
    return queryset

