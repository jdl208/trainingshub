from django.urls import path
from . import views


urlpatterns = [
    path("", views.CourseListView.as_view(), name="course-list"),
    path("training/", views.TrainingListView.as_view(), name="training-list"),
    path("meet-and-greet/", views.MeetGreetListView.as_view(), name="meet-greet-list"),
    path("knowledge-evening/", views.KnowledgeEveningListView.as_view(), name="knowledge-evening-list"),
    path("new/", views.CourseCreateView.as_view(), name="course-create"),
    path("course-type/", views.CourseTypeCreateView.as_view(), name="course-type-create",),
    path("course-type/<int:pk>/update/", views.CourseTypeUpdateView.as_view(), name="course-type-update",),
    path("course-type/<int:id>/delete/", views.delete_course_type, name="course-type-delete",),
    path("location/", views.LocationCreateView.as_view(), name="location-create"),
    path("location/<int:pk>/update/", views.LocationUpdateView.as_view(), name="location-update",),
    path("location/<int:id>/delete/", views.delete_location, name="location-delete"),
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),
]
