from rest_framework import viewsets
from api_files.serializers import FileSerializer, GetFileSerializer
from rest_framework import filters
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope


class FileView(viewsets.ModelViewSet):
    pass
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ['name']
    #
    # required_alternate_scopes = {
    #     "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
    #     "create": [["admin"], ["super_admin"]],
    #     "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
    #     "update": [["admin"], ["super_admin"]],
    #     "partial_update": [["admin"], ["super_admin"]],
    #     "destroy": [["admin"], ["super_admin"]],
    # }
    #
    # def get_permissions(self):
    #     if self.action in ("create", "update", "partial_update", "destroy"):
    #         self.permission_classes = [TokenHasActionScope]
    #     if self.action in ("retrieve", "list"):
    #         self.permission_classes = []
    #     return super(self.__class__, self).get_permissions()
    #
    # queryset = File.objects.all()
    #
    # def get_serializer_class(self, *args, **kwargs):
    #     if self.action == "retrieve":
    #         return GetFileSerializer
    #     return FileSerializer
