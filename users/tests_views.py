from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestUserViews(TestCase):
    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_POST_add_new_user(self):
        response = self.client.post(
            reverse("register"), {"username": "test@test.test", "password1": "testing321", "password2": "testing321"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().username, "test@test.test")

    # def test_logout(self):
    #     self.client.login(username="foo", password="bar")
    #     response = self.client.get("/users/logout/")
    #     self.assertEqual(response.status_code, 302)
