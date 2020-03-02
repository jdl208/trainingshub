from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("complaints/", views.complaints, name="complaints"),
    path("payment/", views.payment, name="payment"),
    path("pickup-service", views.pickup_service, name="pickup-service"),
    path("privacy/", views.privacy, name="privacy"),
]
