import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from courses.models import Courses
from trainingshub import settings

from .forms import MakePaymentForm, SignupForm
from .models import Signup

stripe.api_key = settings.STRIPE_SECRET


@login_required
def signup(request, id):
    course = Courses.objects.get(pk=id)

    # signup for course without paying
    if request.method == "POST" and "confirm" in request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"You have successfully registerd for {course.name}!"
            )
            return redirect("account")

    # signup for course and pay via payment provider
    elif request.method == "POST" and "pay" in request.POST:
        signup_form = SignupForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if signup_form.is_valid() and payment_form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=int(course.costs * 100),
                    currency="EUR",
                    description=request.user.username,
                    card=payment_form.cleaned_data["stripe_id"],
                )
                messages.info(request, "I tried!")
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                signup = signup_form.save(commit=False)
                signup.paid = True
                signup.save()
                messages.success(request, "You have succesfully paid!")
                return redirect(reverse("courses"))

            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")

    # Generate the signup form with prefilled fields
    if Signup.objects.filter(course=course).filter(registrant=request.user):
        messages.info(request, f"Already signed up for this course!")
        signedup = True
    else:
        signedup = False
    signup_form = SignupForm(
        initial={
            "course": course.id,
            "registrant": f"{request.user.id}",
            "address": f"{request.user.profile.address}",
            "postcode": f"{request.user.profile.postcode}",
            "city": f"{request.user.profile.city}",
        }
    )
    payment_form = MakePaymentForm()
    return render(
        request,
        "signups/signup.html",
        {
            "course": course,
            "s_form": signup_form,
            "signedup": signedup,
            "payment_form": payment_form,
            "publishable": settings.STRIPE_PUBLISHABLE,
        },
    )
