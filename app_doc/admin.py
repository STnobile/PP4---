from django.contrib import admin
from .models import Appointment
# Register your models here.


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


admin.site.register(Appointment, AppointmentAdmin)
