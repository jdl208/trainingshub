from django.db import models
from django.contrib.auth.models import User
from courses.models import Courses


class Signup(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
    full_name = models.CharField(max_length=100, blank=False)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    street_address = models.CharField(max_length=60, blank=False)
    postcode = models.CharField(max_length=7, blank=False)
    city = models.CharField(max_length=50, blank=False)
    additional_information = models.TextField(blank=True)
    date = models.DateField(blank=False)
    cancelled = models.DateField(blank=True)

    def __str__(self):
        return f'{self.id}-{self.full_name}-{self.course.name}'


# class Order(models.Model):
#     course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=False)
#     signup = models.ForeignKey(Signup, on_delete=models.CASCADE, null=False)

#     def __str__(self):
#         return f'{self.course.name}-{self.course.date} @ {self.course.costs}'
