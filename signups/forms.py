from django import forms
from .models import Signup


class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2030)]

    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvc = forms.CharField(label='Security code (CVC)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('course', 'registrant', 'additional_information')
        widgets = {'course': forms.HiddenInput(),
                   'registrant': forms.HiddenInput()}
