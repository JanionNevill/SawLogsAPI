from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from logs.filters import LogFilter
from logs.models import Log
from logs.serializers import LogSerializer


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LogFilter
