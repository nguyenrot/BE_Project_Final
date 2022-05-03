from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_statistic.views import StatisticView

router = DefaultRouter()
router.register(r'', StatisticView, basename='statistic')
urlpatterns = [
    path("", include(router.urls)),
]
