from rest_framework import viewsets
from api_offices.models import Office, Group
from api_offices.serializers import OfficeSerializer, GroupListSerializer
from rest_framework.response import Response
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from api_offices.services import OfficeService
from rest_framework import status


class OfficeView(viewsets.ModelViewSet):
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
        if self.action in ("retrieve", "list", "get_tree_office", "get_select"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    def get_queryset(self):
        return Office.objects.all()

    def get_serializer_class(self):
        return OfficeSerializer

    @action(methods=['get'], detail=False)
    def get_tree_office(self, request):
        queryset = Group.objects.all()
        serializer = GroupListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def get_select(self, request):
        root_group = list()
        groups = Group.objects.filter().values("id",
                                               "name",
                                               "parent_group")
        for group in groups:
            OfficeService.get_select(group)
            root_group.append(group)
        return Response(root_group, status=status.HTTP_200_OK)
