from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_news.views import NewsView

router = DefaultRouter()
router.register(r'', NewsView, basename='news')
urlpatterns = [
    path("", include(router.urls)),
]
