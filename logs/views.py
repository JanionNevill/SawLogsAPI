from django.db.transaction import atomic
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
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

    @action(detail=True, methods=["post"])
    def split(self, request, pk=None):
        log = self.get_object()
        split_length = request.data.get("length")

        if split_length is None:
            return Response(
                {"detail": "Split length is required"}, status=HTTP_400_BAD_REQUEST
            )

        try:
            split_length = int(split_length)
        except ValueError:
            return Response(
                {"detail": "Split length must be an integer"},
                status=HTTP_400_BAD_REQUEST,
            )

        if split_length <= 0 or split_length >= log.length:
            return Response(
                {"detail": "Invalid split length"}, status=HTTP_400_BAD_REQUEST
            )

        if log.reservation is not None:
            return Response(
                {"detail": "Cannot split a reserved log"}, status=HTTP_400_BAD_REQUEST
            )

        with atomic():
            log = Log.objects.select_for_update().get(pk=log.pk)

            new_log = Log.objects.create(
                species=log.species,
                grade=log.grade,
                diameter=log.diameter,
                length=log.length - split_length,
            )

            log.length = split_length
            log.save()

        return Response(
            {
                "original_log": LogSerializer(log).data,
                "new_log": LogSerializer(new_log).data,
            },
            status=HTTP_201_CREATED,
        )
