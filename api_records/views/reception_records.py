from api_records.models import ReceptionRecords
from api_records.serializers import ReceptionRecordsSerializers
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class ReceptionRecordsview(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']

    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    queryset = ReceptionRecords.objects.all()
    serializer_class = ReceptionRecordsSerializers

    def approve(self, requset, pk=None):
        queryset = ReceptionRecords.objects.all()
        reception_record = get_object_or_404(queryset, pk=pk)
        reception_record.approve = True
        reception_record.status = "Đã tiếp nhận"
        return Response("Đã tiếp nhận", status=status.HTTP_200_OK)

    def assignment(self, request, pk=None):
        pass
