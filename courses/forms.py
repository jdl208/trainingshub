from django import forms
from .models import Courses, Course_type, Location


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        widgets = {
            "date": DateInput(),
            "ends": DateInput(),
            "time": TimeInput(),
            "endtime": TimeInput(),
        }


class NewCourseTypeForm(forms.ModelForm):
    class Meta:
        model = Course_type
        fields = "__all__"
        labels = {"name": False}
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Add a new course type.",
                    "aria-label": "New course type",
                    "aria-describedby": "save-course-type",
                    "class": "form-control",
                }
            )
        }


class NewLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
        labels = {
            "name": False,
            "street_address": False,
            "postcode": False,
            "city": False,
            "tel": False,
            "google_maps": False,
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Location name (required)"}),
            "street_address": forms.TextInput(attrs={"placeholder": "Street address (required)"}),
            "postcode": forms.TextInput(attrs={"placeholder": "Postcode (required)"}),
            "city": forms.TextInput(attrs={"placeholder": "Town or city (required)"}),
            "tel": forms.TextInput(attrs={"placeholder": "Telephone number"}),
            "google_maps": forms.URLInput(attrs={"placeholder": "URL on google maps"}),
        }
