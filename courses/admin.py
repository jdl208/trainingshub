from django.contrib import admin
from .models import Location, Courses, Course_type

admin.site.register(Location)
admin.site.register(Course_type)
admin.site.register(Courses)