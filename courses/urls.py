from django.urls import path
from . import views


urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("new-course/", views.CourseCreateView.as_view(), name="course-create"),
    path("new-location/", views.LocationCreateView.as_view(), name="location-create"),
    path(
        "new-course-type/",
        views.CourseTypeCreateView.as_view(),
        name="course-type-create",
    ),
    path(
        "update-course-type/<int:pk>",
        views.CourseTypeUpdateView.as_view(),
        name="course-type-update",
    ),
    path(
        "delete-course-type/<id>", views.delete_course_type, name="course-type-delete",
    ),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
]
