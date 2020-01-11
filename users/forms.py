from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    username = forms.EmailField(max_length=75, label="Email", error_messages={'unique': 'Er is al een account geregistreerd met dit email adres!'})
    first_name = forms.CharField(label='Voornaam', max_length=50)
    last_name = forms.CharField(label='Achternaam', max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()

        return user

class UserUpdateForm(forms.ModelForm):
    username = forms.EmailField(max_length=75, label="Email", error_messages={'unique': 'Er is al een account geregistreerd met dit email adres!'})
    first_name = forms.CharField(label='Voornaam', max_length=50)
    last_name = forms.CharField(label='Achternaam', max_length=50)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


    def save(self, commit=True):
        user = super().save(False)
        user.email = user.username
        user = super().save()

        return user
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'postcode', 'city']