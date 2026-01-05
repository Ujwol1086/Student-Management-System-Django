from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def mark_attendance(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
    return render(request, 'core/attendance.html', {'form': form})
