import django_filters
from .models import Courses


class CoursesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Courses
        fields = [
            "name",
            "ngt",
            "asl",
            "schrijftolk",
            "combitolk",
            "location",
        ]
