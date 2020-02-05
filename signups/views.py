from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Courses
from django.contrib.auth.decorators import login_required
from .forms import SignupForm

@login_required
def signup(request, pk):
    course = Courses.objects.get(pk=pk)
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully registerd for the course {course.name}!')
            return redirect('account')
    else:
        data = {'full_name': f'{request.user.first_name} {request.user.last_name}',
                'postcode': request.user.profile.postcode,
                'city': request.user.profile.city,
                'street_address': request.user.profile.address
                }
        signup_form = SignupForm(initial=data)
    return render(request, 'signups/signup.html', {'course': course,
                                                   's_form': signup_form})