from rest_framework import viewsets
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_evaluates.serializers import EvaluateSerializer
from api_evaluates.models import Evaluate


class EvaluateView(viewsets.ModelViewSet):
    queryset = Evaluate.objects.all()
    serializer_class = EvaluateSerializer

    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    class MyList(list):
        def get(self, index, default=None):
            return self[index] if len(self) > index else default

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list", "create"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()
