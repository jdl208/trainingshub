from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestUserViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test@test.test", password="testing321")
        self.superuser = User.objects.create_superuser(
            username="super@user.com", email="super@user.com", password="testing321"
        )

    def test_register_GET(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_POST_add_new_user(self):
        response = self.client.post(
            reverse("register"), {"username": "test2@test.test", "password1": "testing321", "password2": "testing321"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().username, "test2@test.test")

    def test_logout(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_account(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("account"))
        self.assertEqual(response.status_code, 200)

    def test_profile_GET(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_POST(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "foo",
                "last_name": "bar",
                "username": "test@test.test",
                "company_name": "Blabla",
                "address": "street 1",
                "postcode": "1234AB",
                "city": "Amsterdam",
                "rtgs_nr": 42,
            },
        )
        user = User.objects.get(username="test@test.test")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, "foo")

    def test_userlist(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)

    def test_user_detail(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/users/1/")
        self.assertEqual(response.status_code, 200)

    def test_user_search(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("user-search"), {"q": "test"})
        self.assertEqual(response.status_code, 200)
