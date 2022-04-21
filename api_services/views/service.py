from rest_framework import viewsets, status
from api_services.models import Service
from api_services.serializers import ServiceSerializers, ServiceListSerializers
from api_files.serializers import ServiceComponentSerializers
from rest_framework import filters
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
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

    class MyList(list):
        def get(self, index, default=None):
            return self[index] if len(self) > index else default

    def create(self, request, *args, **kwargs):
        field = request.data.get("field")
        name = request.data.get("name")
        decision_number = request.data.get("decision_number")
        type_procedure = request.data.get("type_procedure")
        code_dvcqg = request.data.get("code_DVCQG")
        sequence = request.data.get("sequence")
        method = request.data.get("method")
        amount = request.data.get("amount")
        object = request.data.get("object")
        result = request.data.get("result")
        receiving_address = request.data.get("receiving_address")
        description = request.data.get("description")
        data = {"field": field, "name": name, "decision_number": decision_number, "type_procedure": type_procedure,
                "code_DVCQG": code_dvcqg, "sequence": sequence, "method": method, "amount": amount, "object": object,
                "result": result, "receiving_address": receiving_address, "description": description}
        service_serializer = ServiceSerializers(data=data)
        if service_serializer.is_valid():
            service_serializer.save()
        else:
            return Response(service_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        id_service = service_serializer.data.get("id")

        ingredient = self.MyList(request.data.getlist('ingredient'))
        original = self.MyList(request.data.getlist('original'))
        copy = self.MyList(request.data.getlist('copy'))
        note = self.MyList(request.data.getlist('note'))
        file_sample = self.MyList(request.data.getlist('file_sample'))

        for i in range(len(ingredient)):
            data = {'service': id_service, 'ingredient': ingredient.get(i), 'original': original.get(i),
                    'copy': copy.get(i), 'file_sample': file_sample.get(i),
                    'note': note.get(i)}

            service_component_serializer = ServiceComponentSerializers(data=data)
            if service_component_serializer.is_valid():
                service_component_serializer.save()
            else:
                return Response(service_component_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(service_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in ("list"):
            return ServiceListSerializers
        return ServiceSerializers

    pagination_class = CustomPagination

    @action(methods=['get'], detail=False)
    def get_services(self, request, *args, **kwargs):
        paginator = CustomPagination()
        id_office = request.GET.get("office")
        id_field = request.GET.get("field")
        search = request.GET.get("search")
        services = Services.get_services(id_office, id_field, search)
        paged_queryset = self.paginate_queryset(services)
        serializer = ServiceListSerializers(paged_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_all(self, request, *args, **kwargs):
        queryset = Service.objects.all()
        paged_queryset = self.paginate_queryset(queryset)
        serializer = ServiceListSerializers(paged_queryset, many=True)
        return self.get_paginated_response(serializer.data)
