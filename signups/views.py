from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Courses
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Signup


@login_required
def signup(request, id):
    course = Courses.objects.get(pk=id)

    # signup for course without paying
    if request.method == 'POST' and 'confirm' in request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully registerd for the course {course.name}!')
            return redirect('account')

    # signup for course and pay via payment provider
    elif request.method == 'POST' and 'pay' in request.POST:
        messages.warning(request, f'Stripe hasn\'t been set up yet. You can register without paying up front.')

    # Generate the signup form with prefilled fields
    if Signup.objects.filter(course=course).filter(registrant=request.user):
        messages.info(request, f'Already signed up for this course!')
        signedup = True
    else:
        signedup = False
    signup_form = SignupForm(initial={'course': course.id,
                                      'registrant': f'{request.user.id}'})
    return render(request, 'signups/signup.html', {'course': course,
                                                   's_form': signup_form,
                                                   'signedup': signedup})
