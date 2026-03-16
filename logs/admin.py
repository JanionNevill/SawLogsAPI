from django.contrib import admin

from logs.models import Log


class LogAdmin(admin.ModelAdmin):
    model = Log
    list_display = ["id", "species", "diameter", "length", "grade"]


admin.site.register(Log, LogAdmin)
