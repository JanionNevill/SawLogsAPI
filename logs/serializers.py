from rest_framework.serializers import ModelSerializer

from logs.models import Log


class LogSerializer(ModelSerializer):
    class Meta:
        model = Log
        fields = ["id", "species", "diameter", "length", "grade"]
