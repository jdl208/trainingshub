from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    address = models.CharField(max_length=50)
    postcode = models.CharField(max_length=6)
    city = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user.email} Profile'

    def save(self):
        super().save()
        # Resize uploaded image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
