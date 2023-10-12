from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from app_doc.models import Appointment


class ManageStaffViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('manage_staff')
        self.user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

    def test_manage_staff_view_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_manage_staff_view_for_authenticated_superuser(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


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