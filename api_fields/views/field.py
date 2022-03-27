from rest_framework import viewsets
from api_fields.models import Field
from api_fields.serializers import FieldSerializers
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters


class FieldView(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list", "get_all"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    queryset = Field.objects.all()
    serializer_class = FieldSerializers

    @action(methods=['get'], detail=False)
    def get_all(self, request):
        queryset = Field.objects.all()
        serializer = FieldSerializers(queryset, many=True)
        return Response(serializer.data)
