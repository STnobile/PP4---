from django.urls import path
from .views import (
    HomeTemplateView,
    AppointmentTemplateView,
    ManageAppointmentTemplateView,
    AppointmentReschedule,
    # AppointmentConfirm,
    AppointmentDelete,
)

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('appointment/', AppointmentTemplateView.as_view(), name='appointment'),
    path('manage/', ManageAppointmentTemplateView.as_view(), name='manage'),
    path('appointment/<int:pk>/reschedule/', AppointmentReschedule.as_view(), name='appointment_reschedule'),
    # path('appointment/<int:pk>/confirm/', AppointmentConfirm.as_view(), name='appointment_confirm'),
    path('appointment/<int:pk>/delete/', AppointmentDelete.as_view(), name='appointment_delete'),
]
