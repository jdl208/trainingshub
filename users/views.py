from datetime import datetime

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect, render, reverse

from signups.models import Signup

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {user}. Please fill in the additional information.")
            return redirect("profile")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def logout(request):
    """ Log the user out """
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse("login"))


@login_required
def account(request):
    context = {
        "upcoming": Signup.objects.filter(registrant=request.user, course__date__gte=datetime.today()),
        "past": Signup.objects.filter(registrant=request.user, course__date__lt=datetime.today()),
        "user": request.user,
    }
    return render(request, "users/user_detail.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated!")
            return redirect("account")
    context = {
        "u_form": UserUpdateForm(instance=request.user),
        "p_form": ProfileUpdateForm(instance=request.user.profile),
    }
    return render(request, "users/profile.html", context)


def is_staff(user):
    """
    Test if user is staff so they can get acces to certain areas of the app.
    """
    return user.is_staff


@user_passes_test(is_staff, login_url="home")
def userlist(request):
    userlist = User.objects.all()
    p = Paginator(userlist, 10)
    page = request.GET.get("page")
    users = p.get_page(page)
    return render(request, "users/users_list.html", {"users": users})


@user_passes_test(is_staff, login_url="home")
def user_detail(request, id):
    context = {
        "user": User.objects.get(pk=id),
        "upcoming": Signup.objects.filter(registrant=id, course__date__gte=datetime.today()).order_by("course__date"),
        "past": Signup.objects.filter(registrant=id, course__date__lt=datetime.today()).order_by("-course__date"),
    }
    return render(request, "users/user_detail.html", context)


@user_passes_test(is_staff, login_url="home")
def user_search(request):
    """
    Search user by username/email, first name or last name
    """
    userlist = User.objects.filter(
        Q(username__icontains=request.GET["q"])
        | Q(first_name__icontains=request.GET["q"])
        | Q(last_name__icontains=request.GET["q"])
    )
    p = Paginator(userlist, 10)
    page = request.GET.get("page")
    users = p.get_page(page)
    return render(request, "users/users_list.html", {"users": users})
