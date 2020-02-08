from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Courses
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Signup


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
        data = {'course': course.id,
                'registrant': f'{request.user.id}',
                }
        if Signup.objects.filter(course=course).filter(registrant=request.user):
            messages.info(request, f'Already signed up for this course!')
            signedup = True
        else:
            signedup = False
        signup_form = SignupForm(initial=data)
    return render(request, 'signups/signup.html', {'course': course,
                                                   's_form': signup_form,
                                                   'signedup': signedup})
