from rest_framework import viewsets
from api_users.models import Role
from api_users.serializers import RoleSerializers
from rest_framework.response import Response


class RoleView(viewsets.ViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    def list(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializers(queryset, many=True)
        return Response(serializer.data)
