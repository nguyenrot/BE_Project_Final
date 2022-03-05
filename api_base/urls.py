from django.urls import path, include, re_path

v1_patterns = [
    path("auth/", include("api_authservices.urls")),
    path("users/", include("api_users.urls")),
    path("oauth2/", include(("api_oauth2.urls", "oauth2"))),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = [
    path("", include(v1_patterns)),
]
