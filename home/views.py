from django.shortcuts import render
from courses.models import Courses
from signups.models import Signup


def home(request):
    if request.user.is_authenticated:
        signedup_list = Signup.objects.filter(registrant=request.user).values_list("course_id", flat=True)
    else:
        signedup_list = []
    for i in signedup_list:
        print(signedup_list)
    context = {"course": Courses.objects.last(), "signedup": signedup_list}
    return render(request, "home/home.html", context)
