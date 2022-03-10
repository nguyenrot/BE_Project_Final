from rest_framework import viewsets
from api_offices.models import Office, Group
from api_offices.serializers import OfficeSerializer, GroupListSerializer
from rest_framework.response import Response
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


class OfficeView(viewsets.ModelViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    pagination_class = None

    def get_queryset(self):
        if self.action == "list":
            return Group.objects.all()
        return Office.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OfficeSerializer
        if self.action == "list":
            return GroupListSerializer
        return OfficeSerializer

    def create(self, request, *args, **kwargs):
        serializer = OfficeSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        return Response(serializer.data)
