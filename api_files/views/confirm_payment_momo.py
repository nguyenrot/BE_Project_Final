from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api_files.models import Payment


class ConfirmPaymentView(viewsets.ViewSet):
    permission_classes = []

    @action(detail=False, methods=["POST"], url_path="")
    def confirm_payment(self, request):
        order_id = request.data.get("orderId")
        request_id = request.data.get("requestId")
        payment = Payment.objects.filter(order_id=order_id, request_id=request_id).first()
        payment.response_time = request.data.get("responseTime")
        payment.message = request.data.get("message")
        payment.result_code = request.data.get("resultCode")
        payment.deep_link = request.data.get("deeplink")
        payment.qr_code_url = request.data.get("qrCodeUrl")
        if payment.result_code == 0:
            payment.record.status = 1
        payment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
