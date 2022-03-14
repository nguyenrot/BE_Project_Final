from rest_framework import serializers
from api_news.models import News


class NewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"
