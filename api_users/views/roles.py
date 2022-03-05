from api_base.views import BaseViewSet
from api_users.models.roles import Role
from api_users.serializers.roles import RoleSerializer
from rest_framework import status
from rest_framework.response import Response


class RoleView(BaseViewSet):
    queryset = Role.objects.exclude(name__exact="Super Administrator")
    serializer_class = RoleSerializer
    required_alternate_scopes = {
        "create": [["role:edit"]],
        "retrieve": [["role:view"]],
        "update": [["role:edit"]],
        "destroy": [["role:edit"]],
        "list": [["role:view"]],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.initial_data.update(
            {"last_modified_by": request.user.username})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.initial_data.update(
            {"last_modified_by": request.user.username})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
