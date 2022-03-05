from oauth2_provider.settings import oauth2_settings

from oauthlib.oauth2.rfc6749.utils import list_to_scope
from rest_framework.serializers import ModelSerializer

from api_oauth2.models import Application


class ApplicationRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = ["scope"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Todo: use get_scopes_backend().get_available_scopes instead of
        if ret.get("scope") == "__all__":
            scopes = list(oauth2_settings.SCOPES)
            scopes_string = list_to_scope(scopes)
            ret.update(scope=scopes_string)
        return ret
