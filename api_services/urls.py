from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_services.views import ServiceView

router = DefaultRouter()
router.register(r'', ServiceView, basename='service')
urlpatterns = [
    path("office/<id_office>/", ServiceView.as_view({"get": "get_services_offices"}),
         name="service_get_services_offices"),
    path("field/<id_field>/", ServiceView.as_view({"get": "get_services_fields"}),
         name="service_get_services_fields"),
    path("", include(router.urls)),
]
