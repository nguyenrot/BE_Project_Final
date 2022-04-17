from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api_files.models import ReceptionRecord


class ConfirmPaymentView(viewsets.ViewSet):
    permission_classes = []

    @action(detail=False, methods=["POST"], url_path="")
    def confirm_payment(self, request):
        order_id = request.data.get("orderId")
        request_id = request.data.get("requestId")
        records = ReceptionRecord.objects.filter(order_id=order_id, request_id=request_id).first()
        records.payment = True
        records.status = 1
        records.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
