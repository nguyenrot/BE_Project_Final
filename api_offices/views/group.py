from rest_framework import viewsets
from api_offices.serializers import GroupSerializer, GroupListSerializer
from api_offices.models import Group, Office
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action


class GroupView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupListSerializer(group)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def get_select(self, request, pk=None):
        office = Office.objects.get(pk=pk)
        offices = Office.objects.filter(parent_office=office).values("id", "name")
        return Response(offices)
