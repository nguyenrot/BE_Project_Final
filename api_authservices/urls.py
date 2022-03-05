from django.urls import path, include

from api_authservices.views import (
    LoginApi,
    RefreshTokenView,
    LogoutView,
)

login_patterns = [
    path("", LoginApi.as_view({"post": "create"}), name="login"),
]

urlpatterns = [
    path("login/", include(login_patterns)),
    path("refresh_token/", RefreshTokenView.as_view(), name="refresh_token"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
