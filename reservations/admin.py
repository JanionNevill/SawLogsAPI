from django.contrib import admin

from logs.models import Log
from reservations.models import Reservation


class LogInline(admin.TabularInline):
    model = Log
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ["__str__", "user", "created_at"]
    list_filter = ["user"]
    inlines = [LogInline]


admin.site.register(Reservation, ReservationAdmin)
