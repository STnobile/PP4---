from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.core.mail import EmailMessage, message
from django.conf import settings
from django.contrib import messages
from .models import Appointment, ContactMessage, Notification
from django.views.generic import ListView
import datetime
import logging
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
import re
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from datetime import date
from django.http import Http404


class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def validate_email(self, email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(email_regex, email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_notifications = 0
        staff_notifications = 0

    # Check if the user is authenticated before trying to fetch notifications
        if self.request.user.is_authenticated:
            # Fetch notification counts using the Notification model
            user_notifications = Notification.objects.filter(
              user=self.request.user, seen=False).count()

        if self.request.user.is_superuser:
            staff_notifications = Notification.objects.filter(
             appointment__accepted=False, seen=False).count()

        context['user_notifications'] = user_notifications

    # Retrieve form_errors from the session and add to context
        form_errors = self.request.session.pop('form_errors', None)
        if form_errors:
            context['form_errors'] = form_errors

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        form_errors = []

        if not name or len(name) < 2:
            form_errors.append('Name must be at least 2 characters long.')
        if not email or not self.validate_email(email):
            form_errors.append('Please provide a valid email address.')
        if not message or len(message) < 10:
            form_errors.append('Message must be at least 10 characters long.')

        if form_errors:
            # Store the form errors in the session
            request.session['form_errors'] = form_errors
            return redirect(reverse('home') + '#contact')
        else:
            # If no error messages, process the data and redirect to the top.
            messages.success(request, 'Email sent successfully!')
            # Email sending logic here...
            return redirect(reverse('home'))


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

        messages.add_message(request, messages.SUCCESS,
                             f"Thanks {fname} for making an appointment, we will email you ASAP!")

        if request.user.is_authenticated:
            Notification.objects.create(
                user=request.user,
                appointment=appointment,
                seen=False,
                message=f"New appointment made by {fname} {lname}."
            )

        return HttpResponseRedirect(request.path)


class ManageAppointmentTemplateView(LoginRequiredMixin, ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    paginate_by = 3

    def post(self, request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.accepted = True
        appointment.accepted_date = date
        appointment.save()

        user_related_to_appointment = User.objects.filter(email=appointment.email).first()

        if user_related_to_appointment:
            Notification.objects.create(
             user=user_related_to_appointment,
             message=f"Your appointment for {appointment.accepted_date} has been accepted.",
             appointment=appointment
            )

        messages.add_message(request, messages.SUCCESS,
                        f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)

    def get_queryset(self):
        # Delete appointments where the reschedule_date is in the past or if there's no reschedule_date and sent_date is in the past
        Appointment.objects.filter(
            models.Q(reschedule_date__lt=date.today()) | 
            models.Q(reschedule_date__isnull=True, sent_date__lt=date.today())
        ).delete()

        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                unaccepted_appointments = Appointment.objects.filter(accepted=False)
                for appointment in unaccepted_appointments:
                    # Reset the notifications related to this appointment
                    related_notifications = Notification.objects.filter(appointment=appointment, seen=False)
                    for notification in related_notifications:
                        notification.seen = True
                        notification.save()
                return Appointment.objects.all()
            else:
                return Appointment.objects.filter(email=user.email)
        else:
            return Appointment.objects.none()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        if not self.request.user.is_superuser:
            appointments = appointments.filter(email=self.request.user.email)

        context.update({
            "title": "Manage Appointments",
            "appointments": appointments
        })
        context['notifications'] = Notification.objects.filter(user=self.request.user, seen=False)
        return context


class UserAppointmentsView(LoginRequiredMixin, ListView):
    template_name = "user_notification.html"
    model = Appointment
    context_object_name = "user_notifications"
    paginate_by = 3

    def get_queryset(self):
        notifications = Notification.objects.filter(
            user=self.request.user,
            seen=False
        ).order_by("-create_time")
        # Mark those notifications as seen
        for notification in notifications:
            notification.seen = True
            notification.save()

        return notifications


class AppointmentReschedule(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Appointment
    fields = ['accepted', 'reschedule_date']
    context_object_name = "app"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.email != self.request.user.email:
            raise Http404("Appointment not found")
        return obj

    def post(self, request, pk):
        date = request.POST.get("date")
        appointment = self.get_object()
        appointment.reschedule_date = date
        appointment.accepted = False
        appointment.accepted_date = None
        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                        f"Request sent for reschedule: {appointment.first_name}")

        Notification.objects.create(
                user=request.user,
                message=f"Your have rescheduled your appointment for {appointment.reschedule_date}.",
                appointment=appointment
            )

        return redirect(reverse("manage"))


class AppointmentDelete(View):
    template_name = 'delete.html'

    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        return render(request, self.template_name, {'appointment': appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        appointment.delete()
        messages.success(
            request, f'Appointment for {appointment.first_name} {appointment.last_name} was canceled.')
        return redirect(reverse_lazy('manage'))


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
            messages.success(
                request, "Appointment rescheduled. The admin will send you a message with the new date.")

        return redirect("manage")


class NotificationView(LoginRequiredMixin, View):
    template_name = 'user_notification.html'

    def get(self, request, *args, **kwargs):
        user_notifications = Notification.objects.filter(user=request.user).order_by('-create_time')
        context = {
            'user_notifications': user_notifications,
        }
        return render(request, self.template_name, context)