from rest_framework import viewsets


class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    filterset_class = None
    filterset_map = {}

    def get_serializer_class(self):
        """
        Get action's serializer base on `serializer_map`
        :return: Serializer
        """
        return self.serializer_map.get(self.action, self.serializer_class)
