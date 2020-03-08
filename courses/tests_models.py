from django.test import TestCase
from .models import Location, Course_type, Courses


class TestLocationModel(TestCase):
    def setUp(self):
        self.loc = Location.objects.create(
            name="Test", street_address="teststreet 12", postcode="1234AA", city="Amsterdam"
        )
        self.ct = Course_type.objects.create(name="Training")
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

    def test_test_location_as_a_string(self):
        self.assertEqual(str(self.loc), "Test - Amsterdam")

    def test_test_course_type_as_a_string(self):
        self.assertEqual(str(self.ct), "Training")

    def test_test_course_as_a_string(self):
        self.assertEqual(str(self.course), "2021-01-01 - Test")
