from rest_framework import serializers


class FileDetailsSerializer(serializers.ModelSerializer):
    pass
    # status_display_value = serializers.CharField(
    #     source="get_status_display", read_only=True
    # )
    # attach = serializers.CharField(default=None, read_only=True)
    #
    # class Meta:
    #     model = FileDetails
    #     fields = "__all__"
    #     extra_fields = ["status_display_value", "attach"]
