from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    
    # Dashboards
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    
    # Attendance
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance/bulk/', views.bulk_attendance, name='bulk_attendance'),
    path('attendance/reports/', views.attendance_reports, name='attendance_reports'),
    path('attendance/per-student/', views.attendance_per_student, name='attendance_per_student'),
    path('attendance/per-student/<int:student_id>/', views.attendance_per_student, name='attendance_per_student_detail'),
    path('attendance/per-course/', views.attendance_per_course, name='attendance_per_course'),
    path('attendance/per-course/<int:course_id>/', views.attendance_per_course, name='attendance_per_course_detail'),
    path('attendance/export/', views.export_attendance, name='export_attendance'),
    
    # Audit Logs
    path('audit-logs/', views.audit_logs, name='audit_logs'),
    
    # Grades
    path('grades/', views.my_grades, name='my_grades'),
    path('grades/manage/', views.manage_grades, name='manage_grades'),
    path('grades/add/', views.add_grade, name='add_grade'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    
    # Calendar/Events
    path('calendar/', views.calendar, name='calendar'),
    path('calendar/add-event/', views.add_event, name='add_event'),
]
