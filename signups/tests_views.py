from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from courses.models import Course_type, Courses, Location
from signups.models import Signup
import stripe


class TestSignupsViews(TestCase):
    def setUp(self):
        self.loc = Location.objects.create(
            name="Test", street_address="teststreet 12", postcode="1234AA", city="Amsterdam"
        )
        self.loc2 = Location.objects.create(
            name="Test2", street_address="teststreet 12", postcode="1234AA", city="Amsterdam"
        )
        self.ct = Course_type.objects.create(name="Training")
        self.ct2 = Course_type.objects.create(name="Test")
        self.course = Courses.objects.create(
            name="Test",
            course_type=self.ct,
            ngt=True,
            credit_language_and_interpreting_skills=1,
            credit_attitude=0,
            credit_target_audiences=0,
            date="2021-01-01",
            time="09:00",
            ends="2021-01-01",
            endtime="17:00",
            costs=100,
            location=self.loc,
            places=12,
            description="This is a test",
        )
        self.user = User.objects.create_user(
            username="test@test.test", email="test@test.test", password="testing321", first_name="John", last_name="Doe"
        )
        self.superuser = User.objects.create_superuser(
            username="super@user.com",
            email="super@user.com",
            password="testing321",
            first_name="Super",
            last_name="User",
        )
        self.signup = Signup.objects.create(
            course=self.course,
            registrant=self.superuser,
            address="Teststreet 1",
            postcode="1234AB",
            city="Rotterdam",
            payment_method="IN",
        )

    def test_signup_view_get(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("signup", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_get_already_signed_up(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("signup", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 302)

    def test_signup_view_post_cc_payment(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.post(
            reverse("signup", kwargs={"id": 1}),
            {
                "course": self.course.id,
                "registrant": f"{self.user.id}",
                "company": "Foobar Inc",
                "address": "Test street 1",
                "postcode": "1234ab",
                "city": "Amsterdam",
                "payment_method": "CC",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Signup.objects.filter(company="Foobar Inc").exists())

    def test_signup_view_post_no_payment(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.post(
            reverse("signup", kwargs={"id": 1}),
            {
                "course": self.course.id,
                "registrant": f"{self.user.id}",
                "company": "Foobar Inc",
                "address": "Test street 1",
                "postcode": "1234ab",
                "city": "Amsterdam",
                "payment_method": "IN",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Signup.objects.filter(company="Foobar Inc").exists())

    def test_signup_list(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("signuplist"))
        self.assertEqual(response.status_code, 200)

    def test_signup_list_completed(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("signuplist-completed"))
        self.assertEqual(response.status_code, 200)

    def test_signup_detail(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("signup-detail", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_checkout_get(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("checkout", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_checkout_get_user_different_from_registrant(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("checkout", kwargs={"id": 1}))
        self.assertEqual(response.status_code, 302)

    # def test_checkout_post_succesfull_payment(self):
    #     self.client.login(username="super@user.com", password="testing321")
    #     response = self.client.post(
    #         reverse("checkout", kwargs={"id": 1}),
    #         {"credit_card_number": "4242424242424242", "cvc": 112, "expiry_month": "1", "expiry_year": "2030"},
    #     )
    #     self.assertEqual(response.status_code, 302)
