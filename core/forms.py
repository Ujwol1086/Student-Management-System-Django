from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Attendance, Course, Student, Grade, Assignment, Event

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'course': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date(), 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'status': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
        }
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError("Cannot mark attendance for future dates.")
        return date

class AttendanceFilterForm(forms.Form):
    """Form for filtering attendance records"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        empty_label="All Courses",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
        empty_label="All Students",
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All'), (True, 'Present'), (False, 'Absent')],
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )

class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance marking"""
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white', 'onchange': 'this.form.submit()'})
    )
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date(), 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'})
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter courses based on user role
        if user:
            from .models import Teacher
            try:
                teacher = Teacher.objects.get(user=user)
                self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
            except Teacher.DoesNotExist:
                if user.is_staff or user.is_superuser:
                    self.fields['course'].queryset = Course.objects.all()
                else:
                    self.fields['course'].queryset = Course.objects.none()
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError("Cannot mark attendance for future dates.")
        return date

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'course', 'assignment_name', 'score', 'max_score', 'due_date', 'submitted_date', 'notes']
        widgets = {
            'student': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'course': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'assignment_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'score': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'max_score': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'submitted_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        max_score = cleaned_data.get('max_score')
        
        if score and max_score:
            if score > max_score:
                raise forms.ValidationError("Score cannot be greater than maximum score.")
            if score < 0:
                raise forms.ValidationError("Score cannot be negative.")
        
        return cleaned_data

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date', 'max_score', 'is_published']
        widgets = {
            'course': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'max_score': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'course', 'start_date', 'end_date', 'event_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'course': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
            'event_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-gray-900 bg-white'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before start date.")
        
        return cleaned_data

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'First name (optional)'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'Last name (optional)'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style all fields with Tailwind classes
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-900',
            'placeholder': 'Confirm password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
