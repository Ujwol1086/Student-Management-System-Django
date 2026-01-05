from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
]
