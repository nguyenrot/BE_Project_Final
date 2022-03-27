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
        if self.action in ("retrieve", "list", "get_services_offices", "get_services_fields"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.action in ("list"):
            return ServiceListSerializers
        return ServiceSerializers

    def get_services_offices(self, request, id_office=None):
        paginator = CustomPagination()
        queryset = Office.objects.all()
        office = get_object_or_404(queryset, pk=id_office)
        services = Service.objects.filter(field__office=office)
        result_page = paginator.paginate_queryset(services, request)
        serializer = ServiceListSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def get_services_fields(self, request, id_field=None):
        paginator = CustomPagination()
        queryset = Field.objects.all()
        field = get_object_or_404(queryset, pk=id_field)
        services = Service.objects.filter(field=field)
        result_page = paginator.paginate_queryset(services, request)
        serializer = ServiceListSerializers(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
