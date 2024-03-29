from django.urls import path
from . import views
from .views import (
    HomeTemplateView,
    AppointmentTemplateView,
    ManageAppointmentTemplateView,
    UserAppointmentsView,
    AppointmentReschedule,
    AppointmentDelete,
    SendMessageView,
    NotificationView
)

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('appointment/', AppointmentTemplateView.as_view(), name='appointment'),
    path('manage/', ManageAppointmentTemplateView.as_view(), name='manage'),
    path('manage_user/', UserAppointmentsView.as_view(), name='manage_user'),
    path('user_appointments/<int:pk>/', UserAppointmentsView.as_view(), name='user_appointments'),
    path('appointment/<int:pk>/reschedule/', AppointmentReschedule.as_view(), name ='appointment_reschedule'),
    path('appointment/<int:pk>/delete/', AppointmentDelete.as_view(), name ='appointment_delete'),
    path('notifications/', NotificationView.as_view(), name='notifications'),
]
