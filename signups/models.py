from django.db import models
from courses.models import Courses
from django.contrib.auth.models import User
from django.utils import timezone


PAYMENT_METHODS = [
    ("CC", "Credit card"),
    ("PIN", "Pin"),
    ("IN", "Invoice"),
]


class Signup(models.Model):
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, null=False, related_name="signup"
    )
    registrant = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=False, null=True)
    postcode = models.CharField(max_length=10, blank=False, null=True)
    city = models.CharField(max_length=100, blank=False, null=True)
    additional_information = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(
        max_length=100, choices=PAYMENT_METHODS, default="CC"
    )
    paid = models.BooleanField(default=False)
    cancelled = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}-{self.registrant}-{self.course}"
