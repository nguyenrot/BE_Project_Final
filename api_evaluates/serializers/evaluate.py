from api_evaluates.models import Evaluate
from rest_framework import serializers


class EvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluate
        fields = "__all__"


class EvaluateCreateSerializer(serializers.Serializer):
    code = serializers.CharField()
    question_1 = serializers.IntegerField()
    question_2 = serializers.IntegerField()
    question_3 = serializers.IntegerField()
    question_4 = serializers.IntegerField()
    question_5 = serializers.IntegerField()
