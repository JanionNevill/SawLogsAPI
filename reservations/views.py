from rest_framework.viewsets import ReadOnlyModelViewSet

from reservations.models import Reservation
from reservations.permissions import IsStaffOrOwner
from reservations.serializers import ReservationSerializer


class ReservationViewSet(ReadOnlyModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsStaffOrOwner]

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)
