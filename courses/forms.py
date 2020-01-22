from django import forms
from .models import Courses


class DateInput(forms.DateInput):
    input_type = 'date'


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'
        widgets = {
            'date': DateInput(),
            'ends': DateInput()
        }