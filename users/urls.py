from django.urls import path
from . import views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', users_views.userlist, name='user_list'),
    path('register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', users_views.logout, name='logout'),
    path('profile/', users_views.profile, name='profile'),
    path('<id>/', users_views.user_detail, name='user-detail'),
]