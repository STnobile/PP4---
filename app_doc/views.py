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


def manage_staff_view(request):
    # Check if the user is authenticated and is a superuser
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    # Get all superusers
    staff_members = User.objects.filter(is_superuser=True)

    # Mark all notifications related to unaccepted and unseen appointments as seen when the superuser accesses the page
    unaccepted_appointments = Appointment.objects.filter(accepted=False)
    for appointment in unaccepted_appointments:
        appointment.reset_notifications()

    # Calculate the notification count (if needed in the context)
    staff_count = Notification.objects.filter(
        seen=False, user=request.user).count()

    context = {
        'staff_members': staff_members,
        'staff_count': staff_count,
    }
    return render(request, 'manage_staff.html', context)


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
            context['staff_notifications'] = staff_notifications
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        form_errors = []  # Initialize an empty list to store any form error messages

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

        if request.user is not AnonymousUser:
            notification = Notification.objects.create(
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
        appointment.reset_notifications()
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
    template_name = "user_appointments.html"
    model = Appointment
    context_object_name = "user_notifications"
    paginate_by = 3

    def get_queryset(self):
        # Get the list of appointments for the logged-in user with notifications
        appointments_with_notifications = Appointment.objects.filter(email=self.request.user.email, notifications__seen=False)

        # Mark those notifications as seen
        for appointment in appointments_with_notifications:
            appointment.notifications.update(seen=True)
        return appointments_with_notifications

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Extract the appointments from the notifications
        context['user_appointments'] = Appointment.objects.filter(email=self.request.user.email, notifications__seen=False)
        return context


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
        previous_accepted_state = appointment.accepted  # Store the previous state
        appointment.accepted = False if 'accepted' not in request.POST else True
        appointment.accepted_date = None
        appointment.user_seen = True
        appointment.reset_notifications()
        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                        f"Request sent for reschedule: {appointment.first_name}")

        # If the superuser has just accepted the rescheduling
        if not previous_accepted_state and appointment.accepted:
            Notification.objects.create(
                 user=appointment.user,
                 message=f"Your reschedule request for {appointment.reschedule_date} has been accepted.",
                 appointment=appointment
                )

        # If the appointment has been rescheduled by the user, notify the superuser
        elif not appointment.accepted:
            superuser = get_user_model().objects.filter(is_superuser=True).first()
            if superuser:  # Check if a superuser exists
                Notification.objects.create(
                 user=superuser,
                 message=f"Appointment with {appointment.first_name} {appointment.last_name} has been rescheduled.",
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
