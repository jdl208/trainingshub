from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Courses
from signups.models import Signup
from .forms import NewCourseForm


class CourseListView(ListView):
    model = Courses

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)  # get the default context data
        context['signedup'] = Signup.objects.filter(registrant=self.request.user)  # add extra field to the context
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
    success_url = '/courses/'
