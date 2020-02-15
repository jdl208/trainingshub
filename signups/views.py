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

    # Go to paymentform before confirming registration
    if request.method == "POST" and request.POST["payment_method"] == "CC":
        s_form = SignupForm(request.POST)
        s_form = s_form.save()
        return redirect("checkout", id=s_form.id)

    # signup for course without paying
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"You have successfully registerd for {course.name}!"
            )
            return redirect("account")

    # Check if user already registerd for the course
    if Signup.objects.filter(course=course).filter(registrant=request.user):
        messages.info(request, f"Already signed up for this course!")
        signedup = True
    else:
        signedup = False

    # Generate the signup form with prefilled fields
    signup_form = SignupForm(
        initial={
            "course": course.id,
            "registrant": f"{request.user.id}",
            "address": f"{request.user.profile.address}",
            "postcode": f"{request.user.profile.postcode}",
            "city": f"{request.user.profile.city}",
        }
    )
    return render(
        request,
        "signups/signup.html",
        {"course": course, "s_form": signup_form, "signedup": signedup,},
    )


@login_required
def checkout(request, id):
    signup = Signup.objects.get(pk=id)
    course = Courses.objects.get(id=signup.course_id)
    # signup for course and pay via payment provider
    if request.method == "POST":
        payment_form = MakePaymentForm(request.POST)

        if payment_form.is_valid():
            try:
                customer = stripe.Charge.create(
                    amount=int(course.costs * 100),
                    currency="EUR",
                    description=request.user.username,
                    card=payment_form.cleaned_data["stripe_id"],
                )
                if customer.paid:
                    messages.success(request, "You have succesfully paid!")
                    signup.paid = True
                    signup.save()
                    return redirect(reverse("course-list"))

                else:
                    messages.error(request, "Unable to take payment")

            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    context = {
        "signup": signup,
        "p_form": MakePaymentForm(),
        "publishable": settings.STRIPE_PUBLISHABLE,
    }
    return render(request, "signups/checkout.html", context)
