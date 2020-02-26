import django_filters as df
from .models import Courses


class CoursesFilter(df.FilterSet):
    name = df.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Courses
        fields = [
            "name",
            "course_type",
            "ngt",
            "asl",
            "schrijftolk",
            "combitolk",
            "location",
        ]
