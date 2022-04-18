from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_files.views import RecordView, ConfirmPaymentView

router = DefaultRouter()
router.register(r'record', RecordView, basename='record')
urlpatterns = [
    path("payment", ConfirmPaymentView.as_view({'post': 'confirm_payment'})),
    path("", include(router.urls)),
]
