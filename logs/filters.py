from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet

from logs.models import Log


class LogFilter(FilterSet):
    diameter_min = NumberFilter(field_name="diameter", lookup_expr="gte")
    diameter_max = NumberFilter(field_name="diameter", lookup_expr="lte")

    class Meta:
        model = Log
        fields = ["species", "grade"]
