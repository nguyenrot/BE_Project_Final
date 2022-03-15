from rest_framework import viewsets
from api_fields.models import Field
from api_offices.models import Office
from api_fields.serializers import FieldSerializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class OfficeFieldView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def retrieve(self, request, id_office=None):
        queryset = Office.objects.all()
        office = get_object_or_404(queryset, pk=id_office)
        fields = Field.objects.filter(office=office)
        serializer = FieldSerializers(fields, many=True)
        return Response(serializer.data)
