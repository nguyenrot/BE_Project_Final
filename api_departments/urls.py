from django.urls import path, include
from api_departments.views import DepartmentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', DepartmentView, basename='department')
urlpatterns = [
    path("", include(router.urls)),
]
