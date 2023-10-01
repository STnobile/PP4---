from django.db import models
from django.http import request
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView


class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=200, default="")
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    reschedule_date = models.DateField(null=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ["-sent_date"]
