from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings


class HomeTemplateView(TemplateView):
    template_name = "index.html"

    def post(self, render):
        name = request.Post.get("name")
        email = request.Post.get("email")
        name = request.Post.get("message")

        email = EmailMessage(
            subject=f"{name} from Clinica Vismara.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Your email has been sent successfully ")
