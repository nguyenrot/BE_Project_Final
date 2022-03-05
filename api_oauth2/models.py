from django.db import models
from oauth2_provider.models import (
    AbstractApplication,
    AbstractGrant,
    AbstractAccessToken,
    AbstractRefreshToken,
)

# Create your models here.
from oauth2_provider.models import AbstractIDToken


class AccessToken(AbstractAccessToken):
    """
    Change token fields from char field to text field (fix token too long)
    """

    token = models.TextField(blank=True)

    class Meta(AbstractAccessToken.Meta):
        swappable = "OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL"


class RefreshToken(AbstractRefreshToken):
    """
    Change token fields from char field to text field (fix token too long)
    """

    token = models.TextField(blank=True)

    class Meta(AbstractRefreshToken.Meta):
        swappable = "OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL"
        unique_together = ()


class Application(AbstractApplication):
    scope = models.TextField(blank=True)

    class Meta(AbstractApplication.Meta):
        swappable = "OAUTH2_PROVIDER_APPLICATION_MODEL"


class Grant(AbstractGrant):
    class Meta(AbstractGrant.Meta):
        swappable = "OAUTH2_PROVIDER_GRANT_MODEL"


class IDToken(AbstractIDToken):
    class Meta(AbstractIDToken.Meta):
        swappable = "OAUTH2_PROVIDER_ID_TOKEN_MODEL"
