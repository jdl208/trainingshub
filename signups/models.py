from django.db import models
from courses.models import Courses
from django.contrib.auth.models import User
from datetime import datetime


class Signup(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
    registrant = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    additional_information = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now)
    cancelled = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}-{self.registrant}-{self.course}'
