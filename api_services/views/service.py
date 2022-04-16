from rest_framework import viewsets
from api_services.models import Service
from api_offices.models import Office
from api_fields.models import Field
from api_services.serializers import ServiceSerializers, ServiceListSerializers
from rest_framework import filters
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from api_base.pagination import CustomPagination
from rest_framework.decorators import action
from api_services.services import Services


class ServiceView(viewsets.ModelViewSet):
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
        if self.action in ("retrieve", "list", "get_services", "get_all"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action in ("list"):
            return ServiceListSerializers
        return ServiceSerializers

    @action(methods=['get'], detail=False)
    def get_services(self, request, *args, **kwargs):
        paginator = CustomPagination()
        id_office = request.GET.get("office")
        id_field = request.GET.get("field")
        search = request.GET.get("search")
        services = Services.get_services(id_office, id_field, search)
        result_page = paginator.paginate_queryset(services, request)
        serializer = ServiceListSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all(self, request, *args, **kwargs):
        paginator = CustomPagination()
        queryset = Service.objects.all()
        serializer = ServiceListSerializers(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
