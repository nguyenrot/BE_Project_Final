from rest_framework import viewsets

from api_files.serializers import FileDetailsSerializer
from rest_framework import filters
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from rest_framework.response import Response
from rest_framework import status


class FileDetailView(viewsets.ModelViewSet):
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
    # queryset = FileDetails.objects.all()
    # serializer_class = FileDetailsSerializer
    #
    # class MyList(list):
    #     def get(self, index, default=None):
    #         return self[index] if len(self) > index else default
    #
    # def create(self, request, *args, **kwargs):
    #     id_file = request.data.get('file')
    #     ingredient = self.MyList(request.data.getlist('ingredient'))
    #     original = self.MyList(request.data.getlist('original'))
    #     copy = self.MyList(request.data.getlist('copy'))
    #     note = self.MyList(request.data.getlist('note'))
    #     id_status = self.MyList(request.data.getlist('status'))
    #     form = self.MyList(request.data.getlist('form'))
    #     for i in range(len(ingredient)):
    #         data = {'file': id_file, 'ingredient': ingredient.get(i), 'original': original.get(i), 'copy': copy.get(i),
    #                 'note': note.get(i), 'status': id_status.get(i), 'form': form.get(i)}
    #         file_serializer = FileDetailsSerializer(data=data)
    #         if file_serializer.is_valid():
    #             file_serializer.save()
    #         else:
    #             return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response("create file detail success", status=status.HTTP_400_BAD_REQUEST)
