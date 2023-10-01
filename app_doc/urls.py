from django.urls import path
from . import views  # <-- Add this import
from .views import (
    HomeTemplateView,
    AppointmentTemplateView,
    ManageAppointmentTemplateView,
    UserAppointmentsView,
    AppointmentReschedule,
    # AppointmentConfirm,
    AppointmentDelete,
    SendMessageView
)

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('appointment/', AppointmentTemplateView.as_view(), name='appointment'),
    path('manage/', ManageAppointmentTemplateView.as_view(), name='manage'),
    path('manage_user/', UserAppointmentsView.as_view(), name='manage_user'),
    path('manage_staff/', views.manage_staff_view, name='manage_staff'),  # Ensure this view function exists in views.py
    path('appointment/<int:pk>/reschedule/', AppointmentReschedule.as_view(), name ='appointment_reschedule'),
    path('appointment/<int:pk>/delete/', AppointmentDelete.as_view(), name ='appointment_delete'),
]
