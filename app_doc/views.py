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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, AnonymousUser
import re
from .models import ContactMessage


def manage_staff_view(request):
    # Check if the user is authenticated and is a superuser
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    # Get all superusers
    staff_members = User.objects.filter(is_superuser=True)
    context = {
        'staff_members': staff_members,
    }
    return render(request, 'manage_staff.html', context)


class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def validate_email(self, email):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(email_regex, email)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts, user_count_b = get_notification_counts(self.request.user)
        context.update(counts)
        context.update(user_count_b)
        context['count'] = user_count_b.get('user_count', 0)
        context['form_errors'] = []
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
            # If form_errors is not empty, re-render the page with the error messages
            context = self.get_context_data(**kwargs)
            context['form_errors'] = form_errors
            return render(request, self.template_name, context)
        else:
            # If form_errors is empty, meaning the form is valid, process the data and redirect
            messages.success(request, 'Email sent successfully!')
            # Email sending logic here
            return redirect('home')


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

        if request.user is not AnonymousUser:
            # Notification.objects.create(user=request.user, appointment=Appointment, message=f"Thanks {fname} for making an appointment, we will email you ASAP!")
            return redirect(reverse("manage"))

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

        data = {
            "fname": appointment.first_name,
            "date": date,
        }

        messages.add_message(request, messages.SUCCESS,
                             f"You accepted the appointment of {appointment.first_name}")
        return HttpResponseRedirect(request.path)

    def get_queryset(self):
        # If the user accessing this view is a superuser, then mark all unaccepted appointments as seen
        if self.request.user.is_superuser:
            unaccepted_appointments = Appointment.objects.filter(
                accepted=False, is_seen=False)
            unaccepted_appointments.update(is_seen=True)
            return Appointment.objects.all()
        else:
            return Appointment.objects.filter(email=self.request.user.email)

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


class UserAppointmentsView(LoginRequiredMixin, ListView):
    template_name = "user_appointments.html"
    model = Appointment
    context_object_name = "user_appointments"
    paginate_by = 3

    def get_queryset(self):
        notifications = Notification.objects.filter(
            user=self.request.user, seen=False).order_by(cred)

        for notification in notifications:
            notification.seen = True

        return notifications


class AppointmentReschedule(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Appointment
    fields = ['accepted', 'reschedule_date']

    context_object_name = "app"
    login_required = True

    def post(self, request, pk):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        appointment = Appointment.objects.get(id=pk)
        appointment.reschedule_date = date
        appointment.accepted = False
        appointment.accepted_date = None
        appointment.save()

        messages.add_message(request, messages.SUCCESS,
                             f"Request sent for reschedule: {appointment.first_name}")

        return redirect(reverse("manage"))


class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('manage')
    template_name = "delete.html"


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


def get_notification_counts(user):
    counts = {'staff_count': 0}
    user_count_b = {'user_count': 0}
    if not user.is_authenticated:
        return counts, user_count_b
    try:
        if user.is_superuser:
            counts['staff_count'] = Appointment.objects.filter(
                accepted=False, is_seen=False).count()
        else:
            user_count_value = Appointment.objects.filter(
                email=user.email, accepted=True, user_is_seen=False).count()
            user_count_b['user_count'] = user_count_value
    except Exception as e:
        print(f"Error getting notification counts: {str(e)}")

    return counts, user_count_b
