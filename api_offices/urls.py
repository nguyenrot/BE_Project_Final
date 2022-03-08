from rest_framework.routers import DefaultRouter
from api_offices.views import OfficeView
from django.urls import path, include

router = DefaultRouter()
router.register(r"", OfficeView, basename="office")
urlpatterns = [
    path("", include(router.urls)),
]
