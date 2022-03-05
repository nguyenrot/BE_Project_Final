import logging

from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import BasePermission

log = logging.getLogger("oauth2_provider")


class CustomTokenMatchesOASRequirements(BasePermission):
    """
    :attr:alternate_required_scopes: dict keyed by HTTP method name with value: iterable alternate scope lists

    This fulfills the [Open API Specification (OAS; formerly Swagger)](https://www.openapis.org/)
    list of alternative Security Requirements Objects for oauth2 or openIdConnect:
      When a list of Security Requirement Objects is defined on the Open API object or Operation Object,
      only one of Security Requirement Objects in the list needs to be satisfied to authorize the request.
    [1](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.0.md#securityRequirementObject)

    For each method, a list of lists of allowed scopes is tried in order and the first to match succeeds.

    @example
    required_alternate_scopes = {
       'GET': [['read']],
       'POST': [['create1','scope2'], ['alt-scope3'], ['alt-scope4','alt-scope5']],
    }

    TODO: DRY: subclass TokenHasScope and iterate over values of required_scope?
    """

    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):  # OAuth 2
            if getattr(token, "scope") == "__all__" and not token.is_expired():
                return True
            required_alternate_scopes = self.get_required_alternate_scopes(
                request, view
            )
            method = request.method.upper()
            if method in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {0}".format(
                        required_alternate_scopes[method]
                    )
                )
                return any(
                    token.is_valid(alt) for alt in required_alternate_scopes[method]
                )
            else:
                log.warning(
                    "no scope alternates defined for method {0}".format(method))
                return True

        assert False, (
            "TokenMatchesOASRequirements requires the"
            "`oauth2_provider.rest_framework.OAuth2Authentication` authentication "
            "class to be used."
        )

    def get_required_alternate_scopes(self, request, view):
        try:
            return getattr(view, "required_alternate_scopes")
        except AttributeError:
            raise ImproperlyConfigured(
                "TokenMatchesOASRequirements requires the views to"
                " define the required_alternate_scopes attribute"
            )


class TokenHasActionScope(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if not token:
            return False

        if hasattr(token, "scope"):  # OAuth 2
            required_alternate_scopes = self.get_required_alternate_scopes(
                request, view
            )
            action = view.action.lower()
            if action in required_alternate_scopes:
                log.debug(
                    "Required scopes alternatives to access resource: {0}".format(
                        required_alternate_scopes[action]
                    )
                )
                return any(
                    token.is_valid(alt) for alt in required_alternate_scopes[action]
                )
            else:
                log.warning(
                    "no scope alternates defined for method {0}".format(action))
                return True

        assert False, (
            "TokenMatchesOASRequirements requires the"
            "`oauth2_provider.rest_framework.OAuth2Authentication` authentication "
            "class to be used."
        )

    def get_required_alternate_scopes(self, request, view):
        try:
            return getattr(view, "required_alternate_scopes")
        except AttributeError:
            raise ImproperlyConfigured(
                "TokenHasActionScope requires the views to"
                " define the required_alternate_scopes attribute"
            )
