# app_doc/context_processors.py
from django.db.utils import OperationalError, ProgrammingError
import logging

from .models import Notification  # Appointment import not used here

logger = logging.getLogger(__name__)

def get_notification(request):
    """
    Safe notification counter for templates.
    Never raises — returns {'count': 0} on any problem so pages still render.
    """
    try:
        user = getattr(request, "user", None)
        if not getattr(user, "is_authenticated", False):
            return {"count": 0}

        count = Notification.objects.filter(user=user, seen=False).count()
        return {"count": count}

    except (OperationalError, ProgrammingError):
        # DB not ready / migrations not applied yet (e.g., first boot, collectstatic)
        logger.warning("get_notification: database not ready; returning 0")
        return {"count": 0}

    except Exception:
        logger.exception("get_notification failed unexpectedly; returning 0")
        return {"count": 0}