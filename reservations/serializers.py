from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from logs.serializers import LogSerializer
from reservations.models import Reservation


class ReservationSerializer(ModelSerializer):

    user = CharField(source="user.username", read_only=True)
    log_set = LogSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at", "log_set"]
