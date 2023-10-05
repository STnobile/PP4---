from .models import Appointment
from django.contrib.auth import get_user_model
import logging

# Configuring logging
logger = logging.getLogger(__name__)


def get_notification(request):
    count = 0  # initializing the count

    if request.user.is_authenticated:
        try:
            # Try to count the relevant appointments
            # count = Appointment.objects.filter(
            #     email=request.user.email, 
            #     accepted=True, 
            #     user_is_seen=False
            # ).count()
            count = Notification.objects.filter(
                user=user,
                seen=False
            ).count()
        except Exception as e:
            # Log any error that occurs
            logger.error(f"Error getting notification count: {str(e)}", exc_info=True)

    data = {"count": count}

    # Use logging instead of print for better practice
    logger.info(f"Notification count: {data}")

    return data