from django.utils import timezone
from oauthlib.common import generate_signed_token
from oauthlib.oauth2.rfc6749.utils import list_to_scope, scope_to_list
from django.contrib.auth import get_user_model


def convert_list_to_space_separated(data: list) -> str:
    return " ".join(data)


def convert_dict_to_space_separated(data: dict) -> str:
    data = list(data.keys())
    return " ".join(data)


def convert_scope_str_to_scope_dict(scopes: str) -> dict:
    scopes = scopes.split(" ")
    if not scopes:
        return scopes
    scopes_dict = {}
    resource_arr = []
    for scope in scopes:
        if scope and scope != "__all__":
            resource = scope.split(":")[0]
            permission = scope.split(":")[1]
            if not scopes_dict.get(resource):
                resource_arr.append(resource)
                scopes_dict[resource] = [permission]
            else:
                scopes_dict.get(resource).append(permission)
    formated_scopes = []
    for key in scopes_dict.keys():
        resource_temp_dict = {}
        resource_temp_dict["scope"] = key
        resource_temp_dict["label"] = key
        children = []
        for permission in scopes_dict.get(key):
            if permission != "super_admin":
                permission_temp_dict = {}
                permission_temp_dict["scope"] = key + ":" + permission
                permission_temp_dict["label"] = permission
                children.append(permission_temp_dict)
        resource_temp_dict["children"] = children
        formated_scopes.append(resource_temp_dict)
    return formated_scopes


def signed_token_generator(private_pem, **kwargs):
    """
    :param private_pem:
    """

    def signed_token_generator(request):
        from core.settings import (
            NBF_TIME,
            DEFAULT_CLIENT_ID,
            DEFAULT_CLIENT_SECRET,
        )

        # now = datetime.utcnow()
        all = set(["__all__"])
        now = timezone.now()
        client_scopes = set(
            get_scopes_backend().get_available_scopes(
                application=request.client, request=request
            )
        )
        scopes = set(request.scopes) if request.scopes is not None else set()

        # Override scope for the default client
        if (
                request.client_id == DEFAULT_CLIENT_ID
                and request.client_secret == DEFAULT_CLIENT_SECRET
                and request.user.roles
        ):
            scopes = set()
            for role in request.user.roles.all():
                scopes = scopes.union(set(scope_to_list(role.scope)))
            default_scopes = set(
                get_scopes_backend().get_default_scopes(
                    application=request.client, request=request
                )
            )
            scopes = scopes.union(default_scopes)
        # limit request scopes
        # if all.issubset(scopes):
        #     scopes = client_scopes
        # valid_scopes = scopes.intersection(client_scopes)
        # request.scope = list(client_scopes)
        request.scope = list(scopes)
        request.claims = kwargs

        request.claims.update(
            {
                "sub": str(request.user.id),
                "iat": now,
                "exp": now + timezone.timedelta(seconds=request.expires_in),
                "nbf": now + timezone.timedelta(seconds=float(NBF_TIME)),
            },
        )
        # request.scopes = list(client_scopes)
        request.scopes = list(scopes)
        return generate_signed_token(private_pem, request)

    return signed_token_generator


def get_scopes_backend():
    from oauth2_provider.settings import oauth2_settings

    scopes_class = oauth2_settings.SCOPES_BACKEND_CLASS
    return scopes_class()
