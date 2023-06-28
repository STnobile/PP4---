from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
from django.template import Context
from django.template.loader import render_to_string, get_template


class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return HttpResponse("Email sent successfully!")


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        subject = request.POST.get("subject")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            subject=subject,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                             f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)


class UserAppointmentsView(ListView):
    template_name = "user_appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = date
        appointment.save()

        data = {
            "fname": appointment.first_name,
            "date": date,
        }

        messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        if not self.request.user.is_superuser:
            appointments = appointments.filter(email=self.request.user.email)

        context.update({
            "title": "Manage Appointments",
            "appointments": appointments
        })
        return context


class AppointmentReschedule(UpdateView):
    template_name = "form.html"
    model = Appointment
    fields = ['accepted', 'reschedule_date']
    # template_name_suffix = "manage"
    context_object_name = "app"
    login_required = True
    # success_url = reverse_lazy('manage')

    def post(self, request, pk):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=pk)
        appointment.reschedule_date = date
        appointment.accepted = False
        appointment.accepted_date = None
        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Request sent for reschedule: {appointment.first_name}")

        return redirect(reverse("manage"))


class AppointmentDelete(DeleteView):
    model = Appointment
    success_url = reverse_lazy('manage')
    template_name = "delete.html"
    login_required = True


class SendMessageView(View):
    def post(self, request):
        appointment_id = request.POST.get("appointment-id")
        date = request.POST.get("date")
        appointment = Appointment.objects.get(id=appointment_id)

        if appointment.rescheduled:
            messages.error(request, "Appointment already rescheduled.")
        else:
            appointment.rescheduled = True
            appointment.sent_date = date
            appointment.save()
            messages.success(request, "Appointment rescheduled. The admin will send you a message with the new date.")

        return redirect("manage")
