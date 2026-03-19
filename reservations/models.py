from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CASCADE


class Reservation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        from logs.models import Log

        logs = Log.objects.filter(reservation=self)
        return f"{self.reference if self.reference is not None else '#' + str(self.id)} - {self.user.username}: {len(logs)} logs"
