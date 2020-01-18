from django import forms
from .models import Courses


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class NewCourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'
        widgets = {
            'starts': DateTimeInput(),
            'ends': DateTimeInput()
        }