from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
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

        email = EmailMessage(
            subject=f"{name} from doctor family.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email sent successfully!")


class AppointmentTemplateView(TemplateView):
    template_name = "appointment.html"

    def post(self, request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
            first_name=fname,
            last_name=lname,
            email=email,
            phone=mobile,
            request=message,
        )

        appointment.save()

        messages.add_message(request, messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)


class ManageAppointmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model = Appointment
    context_object_name = "appointments"
    login_required = True
    paginate_by = 3

    # def post(self, request):
    #     date = request.POST.get("date")
    #     appointment_id = request.POST.get("appointment-id")
    #     appointment = Appointment.objects.get(id=appointment_id)
    #     appointment.accepted = False
    #     appointment.accepted_date = datetime.datetime.now()
    #     appointment.save()

    #     data = {
    #         "fname": appointment.first_name,
    #         "date": date,
    #     }

    #     message = get_template('email.html').render(data)
    #     email = EmailMessage(
    #         "About your appointment",
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [appointment.email],
    #     )
    #     email.content_subtype = "html"
    #     email.send()

    #     messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
    #     return HttpResponseRedirect(request.path)

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



from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# class BookView(DetailView):
#     model = Book

# class BookCreate(CreateView):
#     model = Book
#     fields = ['name', 'pages']
#     success_url = reverse_lazy('book_list')

class AppointmentReschedule(UpdateView):
    model = Appointment
    fields = ['name', 'pages']
    success_url = reverse_lazy('manage')

    # def post(self, request):
    #     date = request.POST.get("date")
    #     appointment_id = request.POST.get("appointment-id")
    #     appointment = Appointment.objects.get(id=appointment_id)
    #     appointment.accepted = True
    #     appointment.accepted_date = datetime.datetime.now()
    #     appointment.save()

    #     data = {
    #         "fname": appointment.first_name,
    #         "date": date,
    #     }

    #     message = get_template('email.html').render(data)
    #     email = EmailMessage(
    #         "About your appointment",
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [appointment.email],
    #     )
    #     email.content_subtype = "html"
    #     email.send()

    #     messages.add_message(request, messages.SUCCESS, f"You accepted the appointment of {appointment.first_name}")
    #     return HttpResponseRedirect(request.path)


class AppointmentCancel(DeleteView):
    model = Appointment
    success_url = reverse_lazy('manage')
    template_name = "delete.html"