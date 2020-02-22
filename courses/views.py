from datetime import datetime
from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import ProtectedError
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from signups.models import Signup
from users.views import is_staff
from .forms import NewCourseForm, NewCourseTypeForm, NewLocationForm
from .models import Courses, Course_type, Location


class CourseListView(ListView):
    model = Courses
    queryset = Courses.objects.filter(date__gte=datetime.today())
    ordering = ["date"]

    def get_context_data(self, **kwargs):
        # get the default context data
        context = super(CourseListView, self).get_context_data(**kwargs)
        # add signed up courses of user to context
        context["signedup"] = Signup.objects.filter(registrant=self.request.user).values_list("course_id", flat=True)
        return context


class CourseDetailView(DetailView):
    model = Courses


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Tests if a user is a staffmember so they can CRUD courses
    """

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class CourseCreateView(StaffRequiredMixin, CreateView):
    """
    If user is staff the she can create new courses.
    """

    model = Courses
    form_class = NewCourseForm


class CourseUpdateView(StaffRequiredMixin, UpdateView):
    """
    If user is staf, she can update the course
    """

    model = Courses
    form_class = NewCourseForm


class CourseDeleteView(StaffRequiredMixin, DeleteView):
    """
    If user is staf, she can delete the course
    """

    model = Courses
    success_url = "/courses/"


class CourseTypeCreateView(StaffRequiredMixin, CreateView):
    """
    If user is staff the she can create new course types.
    """

    template_name = "courses/course_type_form.html"
    model = Course_type
    form_class = NewCourseTypeForm

    def get_success_url(self):
        return reverse("course-type-create")

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Course_type.objects.order_by("name")
        return super(CourseTypeCreateView, self).get_context_data(**kwargs)


class CourseTypeUpdateView(StaffRequiredMixin, UpdateView):
    """
    If user is staff the she can update course types.
    """

    template_name = "courses/course_type_form.html"
    model = Course_type
    form_class = NewCourseTypeForm

    def get_success_url(self):
        return reverse("course-type-create")

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Course_type.objects.order_by("name")
        return super(CourseTypeUpdateView, self).get_context_data(**kwargs)


@user_passes_test(is_staff, login_url="home")
def delete_course_type(request, id):
    try:
        Course_type.objects.get(pk=id).delete()
    except ProtectedError:
        messages.error(
            request, "That course type is in use. You can't delete it!",
        )
    return redirect(reverse("course-type-create"))


class LocationCreateView(StaffRequiredMixin, CreateView):
    """
    If user is staff the she can create add locations where course will take place.
    """

    template_name = "courses/location_form.html"
    form_class = NewLocationForm

    def get_success_url(self):
        return reverse("location-create")

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Location.objects.order_by("name")
        return super(LocationCreateView, self).get_context_data(**kwargs)


class LocationUpdateView(StaffRequiredMixin, UpdateView):
    """
    Update locations where courses take place.
    """

    template_name = "courses/location_form.html"
    model = Location
    form_class = NewLocationForm

    def get_success_url(self):
        return reverse("location-create")

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Location.objects.order_by("name")
        return super(LocationUpdateView, self).get_context_data(**kwargs)


@user_passes_test(is_staff, login_url="home")
def delete_location(request, id):
    """
    Staff members can delete Locations.
    This can only be done when a location is not used in a course.
    """
    try:
        Location.objects.get(pk=id).delete()
    except ProtectedError:
        messages.error(request, "That location is used! Unable to delete!")
    return redirect(reverse("location-create"))
