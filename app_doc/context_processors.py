from .models import Appointment
from django.contrib.auth import get_user_model


def get_notification(request):
    if request.user.is_authenticated:
        count = Appointment.objects.filter(email=request.user.email, accepted=True, user_is_seen=False).count()
    else:
        count = 0
    data = {"count": count}
    print(data)
    return data
