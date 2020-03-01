from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=40)
    rtgs_nr = models.IntegerField(null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"
