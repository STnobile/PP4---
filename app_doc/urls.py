from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView, AppointmentDelete, AppointmentReschedule, AppointmentConfirm, SendMessageView

urlpatterns = [
    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment/",
         AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/",
         ManageAppointmentTemplateView.as_view(), name="manage"),
    path("edit/<int:pk>/", AppointmentReschedule.as_view(), name="appointment_edit"),
    path("appointment/confirm/<int:pk>/",
         AppointmentConfirm.as_view(), name="appointment_confirm"),
    path("delete/<int:pk>/", AppointmentDelete.as_view(),
         name="appointment_delete"),
    path("send-message/", SendMessageView.as_view(), name="send_message"),
]
