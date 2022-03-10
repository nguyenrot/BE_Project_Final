from rest_framework import viewsets
from api_offices.serializers import GroupSerializer, GroupListSerializer
from api_offices.models import Group
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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
