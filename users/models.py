from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=40)
    rtgs_nr = models.IntegerField(unique=True, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')


    def __str__(self):
        return f'{self.user.email} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        # Resize uploaded image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
