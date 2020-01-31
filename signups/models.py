from django.db import models
from django.contrib.auth.models import User
from courses.models import Courses
from datetime import timezone

class Signups(models.Model):
    course = models.OneToOneField(Courses, on_delete=models.CASCADE)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    PAYMENT_CHOICES = [
        ('ID', 'Ideal'),
        ('CC', 'Credit card'),
        ('PI', 'Pin'),
    ]
    payment_method = models.CharField(max_length=2, choices=PAYMENT_CHOICES, default='ID')
    paid = models.BooleanField()
    signup_date = models.DateField(default=timezone.now)
    notes = models.TextField()
    cancelled = models.BooleanField()
