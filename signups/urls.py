from django.urls import path
from . import views


urlpatterns = [
    path("signuplist/", views.signup_list, name="signuplist"),
    path("<id>/", views.signup, name="signup"),
    path("<id>/checkout/", views.checkout, name="checkout"),
]
