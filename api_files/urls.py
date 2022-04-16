from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_files.views import FileView, FileDetailView, RecordView

router = DefaultRouter()
router.register(r'file', FileView, basename='file')
router.register(r'detail', FileDetailView, basename='file_detail')
router.register(r'record', RecordView, basename='record')
urlpatterns = [
    path("", include(router.urls)),
]
