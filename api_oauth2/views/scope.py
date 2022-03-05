from rest_framework.decorators import action
from api_base.views import BaseViewSet
from rest_framework.response import Response
from common.constants.api_oauth2.scope import Scope
from core.settings import SCOPES


class ScopeView(BaseViewSet):
    required_alternate_scopes = {
        "retrieve_all_scopes": [["role:view"]],
    }

    @action(detail=False, methods=["GET"])
    def retrieve_all_scopes(self, request, *args, **kwargs):
        scope_dict = SCOPES
        group = {}
        for key in scope_dict.keys():
            if key != "*":
                resource = Scope.GROUP_SCOPE.get(key.split(":")[0].strip())
                if not resource in group:
                    group[resource] = []
                    group.get(resource).append(
                        {"scope": key, "label": scope_dict.get(key)}
                    )
                else:
                    group.get(resource).append(
                        {"scope": key, "label": scope_dict.get(key)}
                    )
        result = []
        for key in group.keys():
            result.append({"scope": key, "label": key, "children": group[key]})
        return Response({"scope": result})
