from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_files.views import FileView

router = DefaultRouter()
router.register(r'', FileView, basename='file')
urlpatterns = [
    path("", include(router.urls)),
]
