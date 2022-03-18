from api_records.models import ApproveRecords, ReceptionRecords
from api_records.serializers import ApproveRecordsSerializers
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class ApproveRecordsView(viewsets.ModelViewSet):
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

    queryset = ApproveRecords.objects.all()
    serializer_class = ApproveRecordsSerializers

    # def create(self, request, *args, **kwargs):
    #     print(*args)
    #     # uuid_reception_records = request.Data.get("reception_records")
    #     reception_records = ReceptionRecords.objects.get(pk=uuid_reception_records)
    #     reception_records.assignment = True
    #     reception_records.save()
    #     super().create(request, *args, **kwargs)
