from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (
    CharField,
    IntegerField,
    ListField,
    SerializerMethodField,
)
from rest_framework.serializers import ModelSerializer

from logs.models import Log
from reservations.models import Reservation


class ReservationSerializer(ModelSerializer):

    user = CharField(source="user.username", read_only=True)

    logs = SerializerMethodField()
    log_ids = ListField(child=IntegerField(), write_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "user", "created_at", "log_ids", "logs"]
        read_only_fields = ["user", "created_at", "logs"]

    def get_logs(self, obj):
        return [log.id for log in obj.log_set.all()]

    def validate_log_ids(self, id_list):
        if not id_list:
            raise ValidationError(f"Reservation must contain at least one log")

        logs = Log.objects.filter(id__in=id_list)

        if len(logs) < len(id_list):
            existing_log_ids = [log.id for log in logs]
            missing_log_ids = [id for id in id_list if id not in existing_log_ids]
            raise ValidationError(f"Logs: {missing_log_ids} do not exist")

        reserved_logs = logs.filter(reservation__isnull=False)

        reservation_id = self.context["request"].data.get("id")
        if reservation_id is not None:
            reservation = Reservation.objects.filter(id=reservation_id).first()
            reserved_logs = reserved_logs.exclude(reservation=reservation)

        if reserved_logs.exists():
            reserved_ids = [log.id for log in reserved_logs]
            raise ValidationError(f"Logs: {reserved_ids} are already reserved")

        return id_list

    def create(self, validated_data):
        id_list = validated_data.pop("log_ids")
        user = self.context["request"].user

        with atomic():
            # Prevent race condition by locking logs
            logs = Log.objects.select_for_update().filter(id__in=id_list)

            # Create reservation
            reservation = Reservation.objects.create(user=user)

            # Assign logs to reservation
            logs.update(reservation=reservation)

        return reservation

    def update(self, instance, validated_data):
        with atomic():
            current_log_ids = [log.id for log in instance.log_set.all()]
            new_log_ids = validated_data.pop("log_ids")

            # Unreserve logs
            unreserved_log_ids = [
                log for log in current_log_ids if log not in new_log_ids
            ]
            freed_logs = Log.objects.select_for_update().filter(
                id__in=unreserved_log_ids
            )
            freed_logs.update(reservation=None)

            # Reserve new logs
            reserved_log_ids = [
                log for log in new_log_ids if log not in current_log_ids
            ]
            captured_logs = Log.objects.select_for_update().filter(
                id__in=reserved_log_ids
            )
            captured_logs.update(reservation=instance)

            return super().update(instance, validated_data)
