from django.urls import path, include
from api_evaluates.view import EvaluateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', EvaluateView, basename='evaluate')
urlpatterns = [
    path("", include(router.urls)),
]
