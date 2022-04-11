from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_services.views import ServiceView

router = DefaultRouter()
router.register(r'', ServiceView, basename='service')
urlpatterns = [
    path("", include(router.urls)),
]
