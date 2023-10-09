from django.db import models
from django.contrib.auth import get_user_model


class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=200, default="")
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    reschedule_date = models.DateField(null=True, blank=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    user_is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

    def mark_as_seen(self, user):
        """
        Mark the appointment as seen by a superuser or a regular user.
        """
        if user.is_superuser:
            self.is_seen = True
        else:
            self.user_is_seen = True
        self.save()

    def reset_notifications(self):
        """
        Reset the notification flags when an appointment is modified.
        """
        self.is_seen = False
        self.user_is_seen = False
        self.save()

    class Meta:
        ordering = ["-sent_date"]


class Notification(models.Model):
    seen = models.BooleanField(default=False)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.CharField(max_length=255, blank=True, null=True)
    appointment = models.ForeignKey(
        'Appointment',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='notifications'
    )
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - {self.create_time}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_sent}"
