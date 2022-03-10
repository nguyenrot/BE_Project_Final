from rest_framework import viewsets
from api_fields.models import Field
from api_fields.serializers import FieldSerializers
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope


class FieldView(viewsets.ModelViewSet):
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
    queryset = Field.objects.all()
    serializer_class = FieldSerializers
