from rest_framework import viewsets
from api_files.serializers import (
    ReceptionRecordSerializer,
    ReceptionRecordDetailSerializer,
    ViewCustomerRecordSerializer,
    ApproveSerializer,
    ContentSerializer,
)
from api_files.models import ReceptionRecord
from rest_framework.response import Response
from rest_framework import status
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
import random
import string
from api_base.services import SendSms, SendMail
from utils import MomoPayment
from rest_framework.decorators import action
from api_base.pagination import CustomPagination
from django.conf import settings


class RecordView(viewsets.ModelViewSet):
    queryset = ReceptionRecord.objects.all()

    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
        "reception": [["admin"], ["super_admin"], ["employee_receive"]],
        "approve": [["admin"], ["super_admin"], ["employee_approve"]],
        "cancel": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "get_record": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "get_record_not_approve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "get_record_approved": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
    }

    class MyList(list):
        def get(self, index, default=None):
            return self[index] if len(self) > index else default

    def get_permissions(self):
        if self.action in (
                "update", "partial_update", "destroy", "reception", "cancel", "approve", "get_record",
                "get_record_reception", "get_record", "get_record_not_approve", "get_record_approved"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list", "create", "get_record_code"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("retrieve"):
            return ViewCustomerRecordSerializer
        if self.action in ("cancel", "approve"):
            return ContentSerializer
        if self.action in ("reception"):
            return ApproveSerializer
        if self.action in (
                "get_record", "get_record_code", "get_record_reception", "get_record", "get_record_not_approve",
                "get_record_approved"):
            return None
        return ReceptionRecordSerializer

    def create(self, request, *args, **kwargs):
        name_sender = request.data.get("name_sender")
        phone_number = request.data.get("phone_number")
        address = request.data.get("address")
        email = request.data.get("email")
        service = request.data.get("service")
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data_record = {"name_sender": name_sender, "phone_number": phone_number, "address": address, "service": service,
                       "code": code, "email": email}
        record_serializer = ReceptionRecordSerializer(data=data_record)
        if not record_serializer.is_valid():
            return Response(record_serializer.errors)
        record_serializer.save()
        id_record = record_serializer.data.get("id")
        attach = self.MyList(request.data.getlist('attach'))
        service_component = self.MyList(request.data.getlist('service_component'))
        for i in range(len(service_component)):
            data = {'reception_record': id_record, "attach": attach.get(i),
                    "service_component": service_component.get(i)}
            record_detail_serializer = ReceptionRecordDetailSerializer(data=data)
            if record_detail_serializer.is_valid():
                record_detail_serializer.save()
            else:
                return Response(record_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        record = ReceptionRecord.objects.get(pk=id_record)
        if not record.service.amount:
            record.status = 1
            record.save()
            site = settings.HOST_URL
            url = site + "/" + "tracuuhoso/" + str(record.id)
            body = 'Bạn đã nộp hồ sơ {0} thành công.Mã hồ sơ của bạn là {1}'.format(record.service.name, record.code)
            SendSms.send_sms(phone_number=phone_number, body=body)
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
        view_record_serializer = ViewCustomerRecordSerializer(record)
        result = view_record_serializer.data
        if record.status == 0:
            result["pay_url"] = MomoPayment.oder_info(record)
            site = settings.HOST_URL
            url = site + "/" + "tracuuhoso/" + str(record.id)
            body = 'Bạn đã nộp hồ sơ {0} thành công.Mã hồ sơ của bạn là {1}. Hồ sơ này cần phải thanh\
             toán để hoàn tất thủ tục'.format(
                record.service.name, record.code)
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
        return Response(result, status=status.HTTP_201_CREATED)

    pagination_class = CustomPagination

    @action(methods=['get'], detail=False)
    def get_record_code(self, request, *args, **kwargs):
        paginator = CustomPagination()
        code = request.GET.get("code")
        record = ReceptionRecord.objects.filter(code__icontains=code)
        paged_queryset = self.paginate_queryset(record)
        serializer = ReceptionRecordSerializer(paged_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['patch'])
    def reception(self, request):
        id_record = request.data.get("reception_record")
        record = ReceptionRecord.objects.get(pk=id_record)
        if record.status == 2:
            return Response("Hồ sơ {0} đã được tiếp nhận".format(record.code), status=status.HTTP_200_OK)
        if record.status == 4:
            return Response("Hồ sơ {0} đã bị hủy".format(record.code), status=status.HTTP_200_OK)
        if record.status == 0:
            return Response("Hồ sơ {0} chưa thanh toán".format(record.code), status=status.HTTP_200_OK)
        record.status = 2
        record.note = request.data.pop("note", None)
        record.save()
        serializer = ApproveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        site = settings.HOST_URL
        url = site + "/" + "tracuuhoso/" + str(record.id)
        body = 'Mã hồ sơ {0} đã được tiếp nhận thành công.'.format(record.code)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"Hồ sơ {record.code} đã được tiếp nhận",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "Dịch vụ công Epoch Making xin thông báo"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('Tiếp nhận hồ sơ {0} thành công'.format(record.code), status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        record = self.get_object()
        record.status = 4
        record.content = request.data.get("content")
        record.save()
        site = settings.HOST_URL
        url = site + "/" + "tracuuhoso/" + str(record.id)
        body = 'Mã hồ sơ {0} đã bị hủy.'.format(record.code)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"Hồ sơ {record.code} đã bị hủy",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "Dịch vụ công Epoch Making xin thông báo"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('Hủy hồ sơ {0} thành công'.format(record.code), status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        record = self.get_object()
        # if record.approve.user_assignment.id != request.user:
        #     return Response("User này không được chỉ định cho hồ sơ {0}".format(record.code), status=status.HTTP_200_OK)
        if record.status == 1:
            return Response("Hồ sơ {0} chưa được tiếp nhận".format(record.code), status=status.HTTP_200_OK)
        if record.status == 4:
            return Response("Hồ sơ {0} đã bị hủy".format(record.code), status=status.HTTP_200_OK)
        if record.status == 0:
            return Response("Hồ sơ {0} chưa thanh toán".format(record.code), status=status.HTTP_200_OK)
        record.status = 3
        record.content = request.data.get("content")
        record.save()
        site = settings.HOST_URL
        url = site + "/" + "tracuuhoso/" + str(record.id)
        body = 'Mã hồ sơ {0} được duyệt thành công và sẽ sớm được gửi đến địa chỉ {1}.'.format(record.service.name,
                                                                                               record.address)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"Hồ sơ {record.code} được duyệt",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "Dịch vụ công Epoch Making xin thông báo"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('Duyệt hồ sơ {0} thành công'.format(record.code), status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_record(self, request):
        status = request.GET.get("status")
        record = ReceptionRecord.objects.filter(status=status)
        paged_queryset = self.paginate_queryset(record)
        serializer = ReceptionRecordSerializer(paged_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_record_not_approve(self, request):
        record = ReceptionRecord.objects.filter(approve__user_assignment=request.user, status=2)
        paged_queryset = self.paginate_queryset(record)
        serializer = ReceptionRecordSerializer(record, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_record_approved(self, request):
        record = ReceptionRecord.objects.filter(approve__user_assignment=request.user, status=3)
        paged_queryset = self.paginate_queryset(record)
        serializer = ReceptionRecordSerializer(record, many=True)
        return Response(serializer.data)
