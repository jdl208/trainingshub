from django.urls import path
from . import views


urlpatterns = [
    path('<id>/', views.signup, name='signup'),
    path('<id>/checkout/', views.checkout, name='checkout'),

]
