from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from courses.models import Courses
from django.contrib.auth.decorators import login_required
from trainingshub import settings
import stripe
from .forms import SignupForm, MakePaymentForm
from .models import Signup


stripe.api_key = settings.STRIPE_SECRET


@login_required
def signup(request, id):
    course = Courses.objects.get(pk=id)

    # signup for course without paying
    if request.method == 'POST' and 'confirm' in request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully registerd for {course.name}!')
            return redirect('account')

    # signup for course and pay via payment provider
    elif request.method == 'POST' and 'pay' in request.POST:
        signup_form = SignupForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if signup_form.is_valid() and payment_form.is_valid():
            # order = signup_form.save(commit=False)
            # order.date = timezone.now()

            total = course.costs

            try:
                customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id'],

                )
            except stripe.error.CardError:
                messages.error(request, 'Your card was declined!')

            if customer.paid:
                signup = signup_form.save(commit=False)
                signup.paid = True
                signup.save()
                messages.error(request, "You have succesfully paid!")
                return redirect(reverse('courses'))

            else:
                messages.error(request, 'Unable to take payment')
        else:
            print(payment_form.errors)
            messages.error(request, 'We were unable to take a payment with that card!')

    # Generate the signup form with prefilled fields
    if Signup.objects.filter(course=course).filter(registrant=request.user):
        messages.info(request, f'Already signed up for this course!')
        signedup = True
    else:
        signedup = False
    signup_form = SignupForm(initial={'course': course.id,
                                      'registrant': f'{request.user.id}'})
    payment_form = MakePaymentForm()
    return render(request, 'signups/signup.html', {'course': course,
                                                   's_form': signup_form,
                                                   'signedup': signedup,
                                                   'payment_form': payment_form,
                                                   'publishable': settings.STRIPE_PUBLISHABLE})
