from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(max_length=75, label="Email")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()

        return user

class UserUpdateForm(forms.ModelForm):
    username = forms.EmailField(max_length=75, label="Email")

    class Meta:
        model = User
        fields = ['username']


    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()

        return user
    
class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'company_name', 'address', 'postcode', 'city', 'image', 'rtgs_nr']
