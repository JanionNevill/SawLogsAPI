from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from logs.filters import LogFilter
from logs.models import Log
from logs.serializers import LogSerializer


class LogViewSet(ModelViewSet):
    serializer_class = LogSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = LogFilter

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.is_staff:
            return Log.objects.all()
        return Log.objects.filter(reservation=None)
