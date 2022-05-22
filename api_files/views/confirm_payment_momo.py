from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from api_files.models import Payment
from api_base.services import SendSms, SendMail
from django.conf import settings


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
            site = settings.HOST_URL
            url = site + "/" + "tracuuhoso/" + str(record.id)
            body = 'Bạn đã nộp hồ sơ {0} thành công.Mã hồ sơ của bạn là {1}'.format(record.service.name, record.code)
            SendSms.send_sms(phone_number=record.phone_number, body=body)
            mail_data = {
                "template": "mail_templates/mail_successful_file_registration.html",
                "subject": "Đăng ký hồ sơ thành công",
                "context": {
                    "name": record.name_sender,
                    "body": body,
                    "link": url,
                    "title": "Dịch vụ công Epoch Making xin thông báo"
                },
                "to": [record.email],
            }
            SendMail.send_html_email(mail_data)
        if request_code == 1003:
            record.status = 4
            site = settings.HOST_URL
            url = site + "/" + "tracuuhoso/" + str(record.id)
            body = 'Hồ hồ sơ {0}, mã hồ sơ {1} của bạn đã bị hủy do hết thời hạn thanh toán.'.format(
                record.service.name, record.code)
            mail_data = {
                "template": "mail_templates/mail_successful_file_registration.html",
                "subject": "Thông báo hủy hồ sơ",
                "context": {
                    "name": record.name_sender,
                    "body": body,
                    "link": url,
                    "title": "Dịch vụ công Epoch Making xin thông báo"
                },
                "to": [record.email],
            }
            SendMail.send_html_email(mail_data)
        record.save()
        payment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
