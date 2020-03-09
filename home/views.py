from django.shortcuts import render
from courses.models import Courses
from signups.models import Signup


def home(request):
    if request.user.is_authenticated:
        signedup_list = Signup.objects.filter(registrant=request.user).values_list("course_id", flat=True)
    else:
        signedup_list = []
    context = {"course": Courses.objects.last(), "signedup": signedup_list}
    return render(request, "home/home.html", context)


def about(request):
    return render(request, "home/about.html")


def complaints(request):
    return render(request, "home/complaints.html")


def payment(request):
    return render(request, "home/payment.html")


def pickup_service(request):
    return render(request, "home/pickup-service.html")


def privacy(request):
    return render(request, "home/privacy.html")
