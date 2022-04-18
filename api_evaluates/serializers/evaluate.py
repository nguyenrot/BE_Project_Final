from api_evaluates.models import Evaluate
from rest_framework import serializers


class EvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluate
        fields = "__all__"
