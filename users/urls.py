from django.urls import path
from . import views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", users_views.userlist, name="user_list"),
    path("search/", users_views.user_search, name="user-search"),
    path("register/", users_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", users_views.logout, name="logout"),
    path("account/", users_views.account, name="account"),
    path("profile/", users_views.profile, name="profile"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("<id>/", users_views.user_detail, name="user-detail"),
]
