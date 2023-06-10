from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, AppointmentCancel

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/",
         AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/",
         ManageAppointmentTemplateView.as_view(), name="manage"),       
     # path('<pk>/delete/', DeleteView.as_view()),
     #     path('edit/<int:pk>', AppointmentReschedule.as_view(), name='appointment_edit'),
    path('delete/<int:pk>', AppointmentCancel.as_view(), name='appointment_delete'),
]
