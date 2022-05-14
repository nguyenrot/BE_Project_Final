from rest_framework.response import Response
from rest_framework import viewsets
from api_departments.models import Department
from api_departments.serializers import DepartmentSerializer


class DepartmentView(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }
