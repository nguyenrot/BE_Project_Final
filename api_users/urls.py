from rest_framework.routers import DefaultRouter
from api_users.views import UserView, RoleView
from django.urls import path, include

router = DefaultRouter()
router.register(r"", UserView, basename="user")
urlpatterns = [
    path("role/", RoleView.as_view({'get': 'list'}), name="role"),
    path("", include(router.urls)),
]
