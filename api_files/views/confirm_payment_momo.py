from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api_files.models import Payment


class ConfirmPaymentView(viewsets.ViewSet):
    permission_classes = []

    @action(detail=False, methods=["POST"], url_path="")
    def confirm_payment(self, request):
        request_code = request.data.get("resultCode")
        order_id = request.data.get("orderId")
        request_id = request.data.get("requestId")
        payment = Payment.objects.filter(order_id=order_id, request_id=request_id).first()
        payment.response_time = request.data.get("responseTime")
        payment.message = request.data.get("message")
        payment.result_code = request_code
        payment.deep_link = request.data.get("deeplink")
        payment.qr_code_url = request.data.get("qrCodeUrl")
        record = payment.record
        if request_code == 0:
            record.status = 1
        if request_code == 1003:
            record.status = 4
        record.save()
        payment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
