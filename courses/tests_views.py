from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .models import Location, Course_type, Courses


class TestCoursesViews(TestCase):
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

    def test_CourseListView_get_context_data_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("course-list"))
        self.assertIsNotNone(response.context["signedup"])
        self.assertIsNotNone(response.context["filter"])

    def test_CourseListView_get_context_data_when_not_logged_in(self):
        response = self.client.get(reverse("course-list"))
        self.assertIsNotNone(response.context["signedup"])

    def test_TrainingListView_get_context_data_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("training-list"))
        self.assertIsNotNone(response.context["signedup"])
        self.assertIsNotNone(response.context["filter"])

    def test_TrainingListView_get_context_data_when_not_logged_in(self):
        response = self.client.get(reverse("training-list"))
        self.assertIsNotNone(response.context["signedup"])

    def test_MeetGreetListView_get_context_data_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("meet-greet-list"))
        self.assertIsNotNone(response.context["signedup"])
        self.assertIsNotNone(response.context["filter"])

    def test_MeetGreetListView_get_context_data_when_not_logged_in(self):
        response = self.client.get(reverse("meet-greet-list"))
        self.assertIsNotNone(response.context["signedup"])

    def test_KnowledgeEveningListView_get_context_data_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get(reverse("knowledge-evening-list"))
        self.assertIsNotNone(response.context["signedup"])
        self.assertIsNotNone(response.context["filter"])

    def test_KnowledgeEveningListView_get_context_data_when_not_logged_in(self):
        response = self.client.get(reverse("knowledge-evening-list"))
        self.assertIsNotNone(response.context["signedup"])

    def test_CourseDetailView_get_context_data_when_logged_in(self):
        self.client.login(username="test@test.test", password="testing321")
        response = self.client.get("/courses/1/")
        self.assertIsNotNone(response.context["object"])
        self.assertIsNotNone(response.context["signedup"])

    def test_CourseDetailView_get_context_data_when_not_logged_in(self):
        response = self.client.get("/courses/1/")
        self.assertIsNotNone(response.context["signedup"])

    def test_CourseTypeCreateView(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("course-type-create"))
        self.assertIsNotNone(response.context["object_list"])

    def test_user_not_staff(self):
        self.client.login(username="test@test.test", password="testing321")
        self.client.get(reverse("course-type-create"))

    def test_CourseTypeUpdateView(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/course-type/1/update/")
        self.assertIsNotNone(response.context["object_list"])

    def test_CourseType_delete(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/course-type/2/delete/")
        self.assertEqual(response.status_code, 302)

    def test_CourseType_delete_field_in_use(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/course-type/1/delete/")
        self.assertEqual(response.status_code, 302)

    def test_LocationCreateView(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get(reverse("location-create"))
        self.assertIsNotNone(response.context["object_list"])

    def test_LocationUpdateView(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/location/1/update/")
        self.assertIsNotNone(response.context["object_list"])

    def test_Location_delete(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/location/2/delete/")
        self.assertEqual(response.status_code, 302)

    def test_Location_delete_field_in_use(self):
        self.client.login(username="super@user.com", password="testing321")
        response = self.client.get("/courses/location/1/delete/")
        self.assertEqual(response.status_code, 302)
