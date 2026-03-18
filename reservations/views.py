from rest_framework.viewsets import ModelViewSet

from reservations.models import Reservation
from reservations.permissions import IsStaffOrOwner
from reservations.serializers import ReservationSerializer


class ReservationViewSet(ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsStaffOrOwner]

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
