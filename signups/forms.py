from django import forms
from .models import Signup


class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2031)]

    credit_card_number = forms.CharField(label="Credit card number", required=False)
    cvc = forms.CharField(label="Security code (CVC)", required=False)
    expiry_month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(label="Year", choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)


class SignupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = (
            "course",
            "registrant",
            "company",
            "address",
            "postcode",
            "city",
            "additional_information",
            "payment_method",
        )
        labels = {
            "company": False,
            "address": False,
            "postcode": False,
            "city": False,
        }
        widgets = {
            "course": forms.HiddenInput(),
            "registrant": forms.HiddenInput(),
            "company": forms.TextInput(attrs={"placeholder": "Company name"}),
            "address": forms.TextInput(attrs={"placeholder": "Address"}),
            "postcode": forms.TextInput(attrs={"placeholder": "Postcode"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "additional_information": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "If you have a food allergy or anything else we need to know about. Please state it here so we can provide the best service we can.",
                }
            ),
            "payment_method": forms.RadioSelect(),
        }
