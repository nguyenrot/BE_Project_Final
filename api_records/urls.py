from rest_framework.routers import DefaultRouter
from api_records.views import ReceptionRecordsview, ApproveRecordsView
from django.urls import path, include

router = DefaultRouter()
router.register(r"", ReceptionRecordsview, basename="reception_records")
router.register(r"approve_records", ApproveRecordsView, basename="reception_records")
urlpatterns = [
    path("active/<pk>/", ReceptionRecordsview.as_view({"patch": "approve"}),
         name="reception_records_approve"),
    path("assignment/<pk>/", ReceptionRecordsview.as_view({"patch": "assignment"}),
         name="reception_records_assignment"),
    path("", include(router.urls)),
]
