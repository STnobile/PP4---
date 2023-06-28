from django.test import TestCase
from django.urls import reverse
from .models import Appointment
from .views import HomeTemplateView, AppointmentTemplateView
# Create your tests here.


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='admin123'
        )
        self.appointment = Appointment.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            phone='123456789',
            subject='Test Subject',
            request='Test Request'
        )

    def test_home_template_view_post(self):
        response = self.client.post(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Email sent successfully!")

    def test_appointment_template_view_post(self):
        response = self.client.post(reverse('appointment'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(first_name='John', last_name='Doe').exists())

    def test_user_appointments_view(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('user_appointments'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_appointments.html')
        self.assertContains(response, 'John Doe')

    def test_manage_appointment_template_view_post(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'date': '2023-06-01',
            'appointment-id': self.appointment.id
        }
        response = self.client.post(reverse('manage'), data)
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertTrue(self.appointment.accepted)
        self.assertEqual(str(self.appointment.accepted_date), '2023-06-01')

    def test_appointment_reschedule(self):
        self.client.login(username='admin', password='admin123')
        data = {
            'date': '2023-07-01',
            'appointment-id': self.appointment.id
        }
        response = self.client.post(reverse('appointment_reschedule', args=[self.appointment.id]), data)
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertFalse(self.appointment.accepted)
        self.assertEqual(str(self.appointment.reschedule_date), '2023-07-01')

    def test_appointment_delete(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('appointment_delete', args=[self.appointment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Appointment.objects.filter(first_name='John', last_name='Doe').exists())


class TemplateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_manage_appointments_template(self):
        response = self.client.get(reverse('manage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-appointments.html')
