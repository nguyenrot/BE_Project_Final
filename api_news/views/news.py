from rest_framework import viewsets
from api_news.models import News
from api_news.serializers import NewsSerializers
from rest_framework import filters
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope


class NewsView(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title']

    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    queryset = News.objects.all()
    serializer_class = NewsSerializers
