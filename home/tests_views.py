from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User


class TestHomeViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@test.test", password="testing321")

    def test_home_view_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_home_view_when_logged_out(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_static_page_about(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_static_page_complaints(self):
        response = self.client.get(reverse("complaints"))
        self.assertEqual(response.status_code, 200)

    def test_static_page_payment(self):
        response = self.client.get(reverse("payment"))
        self.assertEqual(response.status_code, 200)

    def test_static_page_pickup_service(self):
        response = self.client.get(reverse("pickup-service"))
        self.assertEqual(response.status_code, 200)

    def test_static_page_privacy(self):
        response = self.client.get(reverse("privacy"))
        self.assertEqual(response.status_code, 200)
