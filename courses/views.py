from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Courses


class CourseListView(ListView):
    model = Courses


class CourseDetailView(DetailView):
    model = Courses


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    # Tests if a user is a staffmember so they can CRUD courses
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class CourseCreateView(StaffRequiredMixin, CreateView):
    model = Courses
    fields =['name',
             'course_type',
             'ngt',
             'schrijftolk',
             'asl',
             'combitolk',
             'credit_language_and_interpreting_skills',
             'credit_attitude',
             'credit_target_audiences',
             'starts',
             'ends',
             'costs',
             'location',
             'description',
             'places',
             'image',
             ]

    
class CourseUpdateView(StaffRequiredMixin, UpdateView):
    model = Courses
    fields =['name',
             'course_type',
             'ngt',
             'schrijftolk',
             'asl',
             'combitolk',
             'credit_language_and_interpreting_skills',
             'credit_attitude',
             'credit_target_audiences',
             'starts',
             'ends',
             'costs',
             'location',
             'description',
             'places',
             'image',
             ]


class CourseDeleteView(StaffRequiredMixin, DeleteView):
    model = Courses
    success_url = '/courses/'