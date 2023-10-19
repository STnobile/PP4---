from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from app_doc.models import Appointment, Notification
from datetime import date


class HomeTemplateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def test_home_template_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_template_view_post_invalid_data(self):
        response = self.client.post(self.url, {'name': 'a', 'email': 'invalid', 'message': 'short'})
        self.assertEqual(response.status_code, 302)
        # Add more assertions to check for form errors in the session or messages

    def test_post_valid_data_sends_message(self):
        data = {'name': 'Test Name', 'email': 'test@example.com', 'message': 'Hello, this is a test message with more than 10 characters.'}
        response = self.client.post(self.url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Email sent successfully!')    


class AppointmentTemplateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('appointment')

    def test_appointment_template_view_post(self):
        data = {
            'fname': 'John',
            'lname': 'Doe',
            'email': 'john@example.com',
            'mobile': '123456789',
            'subject': 'Test Subject',
            'request': 'Test Request Message',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Appointment.objects.count(), 1)


class AppointmentRescheduleTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pass', email='user@example.com')
        self.superuser = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        self.appointment = Appointment.objects.create(email=self.user.email, first_name="John", last_name="Doe")

        # URL for rescheduling this appointment
        self.url = reverse('appointment_reschedule', args=[self.appointment.pk])

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirected to login

    def test_only_owner_can_reschedule(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)  # Redirected since not owner

    def test_reschedule_appointment(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(self.url, {'date': '2023-11-20', 'accepted': True})

        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.reschedule_date, date(2023, 11, 20))
        self.assertTrue(self.appointment.accepted)

        # Check success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), f"Request sent for reschedule: {self.appointment.first_name}")

    def test_notification_creation_on_acceptance(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(self.url, {'date': '2023-11-20', 'accepted': True})

        notification = Notification.objects.latest('id')
        expected_user = User.objects.filter(email=self.appointment.email).first()
        self.assertEqual(notification.user, expected_user)
