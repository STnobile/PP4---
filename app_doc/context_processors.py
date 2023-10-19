from .models import Appointment, Notification
from django.contrib.auth import get_user_model
import logging

# Configuring logging
logger = logging.getLogger(__name__)


def get_notification(request):
    count = 0

    if request.user.is_authenticated:
        try:
            # Use request.user instead of user
            notifications = Notification.objects.filter(
                user=request.user,
                seen=False
            )
            count = notifications.count()
        except Exception as e:
            # Log any error that occurs
            logger.error(f"Error getting notification count: {str(e)}", exc_info=True)

    data = {"count": count}

    # Use logging instead of print for better practice
    logger.info(f"Notification count: {data}")

    return data
