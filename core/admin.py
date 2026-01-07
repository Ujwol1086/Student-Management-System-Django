from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import (
    Student, Teacher, Course, Attendance, AuditLog, 
    Grade, Notification, Assignment, Event
)

# Custom User Admin with Teacher/Student selection
class UserCreationForm(forms.ModelForm):
    """Custom user creation form with role selection"""
    USER_TYPE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Administrator'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=True,
        help_text="Select the type of user to create. This will automatically set appropriate permissions."
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Enter a strong password."
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user_type = self.cleaned_data.get('user_type')
        
        if user_type == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif user_type == 'teacher':
            user.is_staff = False
            user.is_superuser = False
        elif user_type == 'student':
            user.is_staff = False
            user.is_superuser = False
        
        if commit:
            user.save()
        return user

class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Use custom form for adding users"""
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Student Admin
class StudentAdminForm(ModelForm):
    """Custom form for Student with user creation"""
    
    create_user = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Check to automatically create a User account for this student."
    )
    username = forms.CharField(
        required=False,
        max_length=150,
        help_text="Username for the new user account (required if creating new user)"
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Password for the new user account (required if creating new user)"
    )
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        create_user = cleaned_data.get('create_user', False)
        username = cleaned_data.get('username', '').strip()
        password = cleaned_data.get('password', '').strip()
        
        if create_user:
            if not username:
                raise ValidationError({'username': 'Username is required when creating a new user account.'})
            if User.objects.filter(username=username).exists():
                raise ValidationError({'username': 'A user with this username already exists.'})
            if not self.instance.pk and not password:
                raise ValidationError({'password': 'Password is required when creating a new user account.'})
        
        return cleaned_data

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('name', 'roll_no', 'email', 'user', 'has_user_account', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'roll_no', 'email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Student Information', {
            'fields': ('name', 'roll_no', 'email', 'dob')
        }),
        ('User Account', {
            'fields': ('user', 'create_user', 'username', 'password'),
            'description': 'Create a new user account or link to an existing one.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_user_account(self, obj):
        return bool(obj.user)
    has_user_account.short_description = "Has Login"
    has_user_account.boolean = True
    
    def save_model(self, request, obj, form, change):
        create_user = form.cleaned_data.get('create_user', False)
        username = form.cleaned_data.get('username', '').strip()
        password = form.cleaned_data.get('password', '').strip()
        
        if create_user and username and not obj.user:
            user = User.objects.create_user(
                username=username,
                email=obj.email,
                password=password,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            obj.user = user
        
        super().save_model(request, obj, form, change)

# Teacher Admin
class TeacherAdminForm(ModelForm):
    """Custom form for Teacher with user creation"""
    
    create_user = forms.BooleanField(
        required=False,
        initial=True,
        help_text="Check to automatically create a User account for this teacher."
    )
    username = forms.CharField(
        required=False,
        max_length=150,
        help_text="Username for the new user account (required if creating new user)"
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=True),
        help_text="Password for the new user account (required if creating new user)"
    )
    
    class Meta:
        model = Teacher
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        create_user = cleaned_data.get('create_user', False)
        username = cleaned_data.get('username', '').strip()
        password = cleaned_data.get('password', '').strip()
        
        if create_user:
            if not username:
                raise ValidationError({'username': 'Username is required when creating a new user account.'})
            if User.objects.filter(username=username).exists():
                raise ValidationError({'username': 'A user with this username already exists.'})
            if not self.instance.pk and not password:
                raise ValidationError({'password': 'Password is required when creating a new user account.'})
        
        return cleaned_data

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('name', 'email', 'subject', 'user', 'has_user_account', 'course_count', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'user__username')
    readonly_fields = ('course_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Teacher Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('User Account', {
            'fields': ('user', 'create_user', 'username', 'password'),
            'description': 'Create a new user account or link to an existing one.'
        }),
        ('Statistics', {
            'fields': ('course_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_user_account(self, obj):
        return bool(obj.user)
    has_user_account.short_description = "Has Login"
    has_user_account.boolean = True
    
    def course_count(self, obj):
        if obj.pk:
            count = obj.course_set.count()
            return f"{count} course{'s' if count != 1 else ''}"
        return "0 courses"
    course_count.short_description = "Courses Assigned"
    
    def save_model(self, request, obj, form, change):
        create_user = form.cleaned_data.get('create_user', False)
        username = form.cleaned_data.get('username', '').strip()
        password = form.cleaned_data.get('password', '').strip()
        
        if create_user and username and not obj.user:
            user = User.objects.create_user(
                username=username,
                email=obj.email,
                password=password,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            obj.user = user
        
        super().save_model(request, obj, form, change)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'student_count', 'created_at')
    filter_horizontal = ('students',)
    list_filter = ('teacher', 'created_at')
    search_fields = ('name', 'code', 'teacher__name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Course Information', {
            'fields': ('name', 'code', 'teacher', 'description')
        }),
        ('Students', {
            'fields': ('students',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_count(self, obj):
        if obj.pk:
            count = obj.students.count()
            return f"{count} student{'s' if count != 1 else ''}"
        return "0 students"
    student_count.short_description = "Enrolled Students"

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'marked_by', 'created_at')
    list_filter = ('course', 'date', 'status', 'course__teacher', 'created_at')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('student__name', 'course__name', 'student__roll_no')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'course', 'date', 'status', 'marked_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'student', 'course', 'date', 'user', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'course')
    search_fields = ('student__name', 'course__name', 'user__username')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Audit logs are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Audit logs should not be modified

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'assignment_name', 'score', 'max_score', 'grade', 'due_date')
    list_filter = ('course', 'grade', 'due_date', 'created_at')
    search_fields = ('student__name', 'course__name', 'assignment_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Grade Information', {
            'fields': ('student', 'course', 'assignment_name', 'score', 'max_score', 'grade')
        }),
        ('Dates', {
            'fields': ('due_date', 'submitted_date')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'max_score', 'is_published', 'created_at')
    list_filter = ('course', 'is_published', 'due_date', 'created_at')
    search_fields = ('title', 'course__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Assignment Information', {
            'fields': ('course', 'title', 'description', 'max_score', 'is_published')
        }),
        ('Dates', {
            'fields': ('due_date',)
        }),
        ('Additional Information', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'event_type', 'start_date', 'end_date', 'created_by')
    list_filter = ('event_type', 'course', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'course__name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'course', 'event_type')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Additional Information', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
