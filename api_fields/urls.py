from django.urls import path, include
from api_fields.views import FieldView, OfficeFieldView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', FieldView, basename='field')
urlpatterns = [
    path("office/<id_office>/", OfficeFieldView.as_view({"get": "retrieve"}), name="field_retrieve"),
    path("", include(router.urls)),
]
