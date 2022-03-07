from rest_framework import serializers
from api_departments.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    def get_slug(self, department):
        return department.get_slug()

    class Meta:
        model = Department
        fields = ["id", "code", "name", "discription", "slug"]
