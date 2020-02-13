from django.db import models
from courses.models import Courses
from django.contrib.auth.models import User
from datetime import datetime


class Signup(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
    registrant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    postcode = models.CharField(max_length=10, blank=False, null=True)
    city = models.CharField(max_length=100, blank=False, null=True)
    additional_information = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now)
    paid = models.BooleanField(default=False)
    cancelled = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}-{self.registrant}-{self.course}"
