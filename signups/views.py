from datetime import datetime

import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, reverse
from django.contrib.admin.views.decorators import staff_member_required

from courses.models import Courses
from trainingshub import settings

from .forms import MakePaymentForm, SignupForm
from .models import Signup

stripe.api_key = settings.STRIPE_SECRET


@login_required
def signup(request, id):
    """
    Create a signup form for the selected course.
    """
    course = Courses.objects.get(pk=id)

    # If user us already signed up for course. Redirect to the course list
    if Signup.objects.filter(course=course).filter(registrant=request.user):
        messages.info(request, f"You already signed up for the course: {course.name} !")
        return redirect("course-list")
    else:
        signedup = False

    # Go to paymentform before confirming registration
    if request.method == "POST" and request.POST["payment_method"] == "CC":
        form = SignupForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect("checkout", id=form.id)

    # signup for course without paying
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"You have successfully registerd for {course.name}!")
            return redirect("account")

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
    return render(request, "signups/signup.html", {"course": course, "s_form": signup_form, "signedup": signedup},)


@login_required
def checkout(request, id):
    """
    Create a payment form for the selected course. Right now they can only pay by credit card.
    """
    signup = Signup.objects.get(pk=id)
    course = Courses.objects.get(id=signup.course_id)

    if signup.registrant != request.user:
        return redirect(reverse("home"))
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


@staff_member_required(login_url="home")
def signup_list(request):
    """
    Generate a list with all the upcoming courses. Sorted first coming date first.
    """
    context = {
        "courses": Courses.objects.filter(date__gte=datetime.today()).order_by("date"),
        "title": "Upcoming courses",
    }
    return render(request, "signups/course-signup-list.html", context)


@staff_member_required(login_url="home")
def signup_list_completed(request):
    """
    Generate a list with all the upcoming courses. Sorted latest date first
    """
    context = {
        "courses": Courses.objects.filter(date__lt=datetime.today()).order_by("-date"),
        "title": "Completed courses",
    }
    return render(request, "signups/course-signup-list.html", context)


@staff_member_required(login_url="home")
def signup_detail(request, id):
    """
    Generate a list with all the upcoming courses. Sorted latest date first
    """
    context = {
        "course": Courses.objects.get(pk=id),
        "signups": Signup.objects.filter(course_id=id),
    }
    return render(request, "signups/course-signup-detail.html", context)
