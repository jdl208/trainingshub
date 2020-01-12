from django.urls import path
from . import views as courses_views


urlpatterns = [
    path('', courses_views.CourseListView.as_view(), name='courses'),
]