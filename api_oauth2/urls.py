from django.urls import path
from api_oauth2.views import ScopeView

urlpatterns = [
    path(
        "retrieve_all_scopes/",
        ScopeView.as_view({"get": "retrieve_all_scopes"}),
        name="scope",
    ),
]
