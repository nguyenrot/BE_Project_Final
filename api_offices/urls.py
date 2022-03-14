from rest_framework.routers import DefaultRouter
from api_offices.views import OfficeView, GroupView
from django.urls import path, include

router = DefaultRouter()
router.register(r"", OfficeView, basename="office")
urlpatterns = [
    path("group/", GroupView.as_view({"get": "list"}), name="group_list"),
    path("group/<pk>", GroupView.as_view({"get": "retrieve"}), name="group_retrieve"),
    path("get_select/<pk>", GroupView.as_view({"get": "get_select"}), name="group_get_select"),
    path("", include(router.urls)),
]
