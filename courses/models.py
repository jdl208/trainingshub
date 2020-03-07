from django.db import models
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=75)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, null=True, blank=True)
    google_maps = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Course_type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Courses(models.Model):
    name = models.CharField(max_length=150)
    course_type = models.ForeignKey(Course_type, on_delete=models.PROTECT, null=False)
    ngt = models.BooleanField(default=False)
    schrijftolk = models.BooleanField(default=False)
    asl = models.BooleanField(default=False)
    combitolk = models.BooleanField(default=False)
    credit_language_and_interpreting_skills = models.FloatField()
    credit_attitude = models.FloatField()
    credit_target_audiences = models.FloatField()
    date = models.DateField()
    time = models.TimeField()
    ends = models.DateField()
    endtime = models.TimeField()
    costs = models.DecimalField(decimal_places=2, max_digits=7)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    places = models.IntegerField(default=0)
    description = models.TextField(null=True)
    image = models.ImageField(default="course-default.svg", upload_to="course_pics")

    def __str__(self):
        return f"{self.date} - {self.name}"

    def get_absolute_url(self):
        return reverse("course-detail", kwargs={"pk": self.pk})
