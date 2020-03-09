from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from courses.models import Course_type, Courses, Location
from signups.models import Signup


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
        self.user = User.objects.create_user(username="test@test.test", password="testing321")
        self.superuser = User.objects.create_superuser(
            username="super@user.com", email="super@user.com", password="testing321"
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
        response = self.client.get("/signup/1/")
        self.assertEqual(response.status_code, 200)

    def test_signup_view_get_already_signed_up(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/signup/1/")
        self.assertEqual(response.status_code, 302)

    # def test_signup_view_post_cc_payment(self):
    #     self.client.login(username="test@test.test", password="testing321")
    #     response = self.client.post(
    #         "/signup/1/",
    #         {
    #             "course": self.course,
    #             "registrant": self.user,
    #             "address": "Teststreet 1",
    #             "postcode": "1234AB",
    #             "city": "Rotterdam",
    #             "payment_method": "CC",
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)
