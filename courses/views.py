from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from signups.models import Signup
from .forms import NewCourseForm
from .models import Courses


class CourseListView(ListView):
    model = Courses
    queryset = Courses.objects.filter(date__gte=datetime.today())
    ordering = ["date"]

    def get_context_data(self, **kwargs):
        # get the default context data
        context = super(CourseListView, self).get_context_data(**kwargs)
        # add signed up courses of user to context
        context["signedup"] = Signup.objects.filter(
            registrant=self.request.user
        ).values_list("course_id", flat=True)
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
