from rest_framework import serializers
from api_evaluates.models import Evaluate


class EvaluateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Evaluate
        fields = "__all__"
