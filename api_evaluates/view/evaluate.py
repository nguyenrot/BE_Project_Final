from rest_framework import viewsets
from api_evaluates.models import Evaluate
from api_evaluates.serializers import EvaluateSerializers
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope


class EvaluateView(viewsets.ModelViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"]],
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

    queryset = Evaluate.objects.all()
    serializer_class = EvaluateSerializers
