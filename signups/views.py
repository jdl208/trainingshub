from django.shortcuts import render
from courses.models import Courses
from .forms import SignupForm

def signup(request, pk):
    course = Courses.objects.get(pk=pk)
    signup_form = SignupForm()
    return render(request, 'signups/signup.html', {'course': course,
                                                   's_form': signup_form})