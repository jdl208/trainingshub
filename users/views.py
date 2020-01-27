from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth, messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def logout(request):
    """ Log the user out """
    auth.logout(request)
    messages.success(request, "You have successfully been logged out!")
    return redirect(reverse('login'))


@login_required
def account(request):
    user = request.user
    return render(request, 'users/user_detail.html', {'user': user})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

def is_staff(user):
    """
    Test if user is staff so they can get acces to certain areas of the app.
    """
    return user.is_staff

@user_passes_test(is_staff, login_url='home')
def userlist(request):
    userlist = User.objects.all()
    p = Paginator(userlist, 10)
    page = request.GET.get('page')
    users = p.get_page(page)
    return render(request, 'users/users_list.html', {'users': users})


@user_passes_test(is_staff, login_url='home')
def user_detail(request, id):
    user = User.objects.get(pk=id)
    return render(request, 'users/user_detail.html', {'user':user})
    

def user_search(request):
    """
    Search user by username/email, first name or last name
    """
    userlist = User.objects.filter(
        Q(username__icontains=request.GET['q']) |
        Q(first_name__icontains=request.GET['q']) |
        Q(last_name__icontains=request.GET['q'])
        )
    p = Paginator(userlist, 10)
    page = request.GET.get('page')
    users = p.get_page(page)
    return render(request, 'users/users_list.html', {'users': users })
