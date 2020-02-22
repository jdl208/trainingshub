from django import forms
from .models import Courses, Course_type


class DateInput(forms.DateInput):
    input_type = "date"


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        widgets = {"date": DateInput(), "ends": DateInput()}


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
    pass
