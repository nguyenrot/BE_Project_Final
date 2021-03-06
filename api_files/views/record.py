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
            body = 'B???n ???? n???p h??? s?? {0} th??nh c??ng.M?? h??? s?? c???a b???n l?? {1}'.format(record.service.name, record.code)
            SendSms.send_sms(phone_number=phone_number, body=body)
            mail_data = {
                "template": "mail_templates/mail_successful_file_registration.html",
                "subject": "????ng k?? h??? s?? th??nh c??ng",
                "context": {
                    "name": record.name_sender,
                    "body": body,
                    "link": url,
                    "title": "D???ch v??? c??ng Epoch Making xin th??ng b??o"
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
            body = 'B???n ???? n???p h??? s?? {0} th??nh c??ng.M?? h??? s?? c???a b???n l?? {1}. H??? s?? n??y c???n ph???i thanh\
             to??n ????? ho??n t???t th??? t???c'.format(
                record.service.name, record.code)
            mail_data = {
                "template": "mail_templates/mail_successful_file_registration.html",
                "subject": "????ng k?? h??? s?? th??nh c??ng",
                "context": {
                    "name": record.name_sender,
                    "body": body,
                    "link": url,
                    "title": "D???ch v??? c??ng Epoch Making xin th??ng b??o"
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
            return Response("H??? s?? {0} ???? ???????c ti???p nh???n".format(record.code), status=status.HTTP_200_OK)
        if record.status == 4:
            return Response("H??? s?? {0} ???? b??? h???y".format(record.code), status=status.HTTP_200_OK)
        if record.status == 0:
            return Response("H??? s?? {0} ch??a thanh to??n".format(record.code), status=status.HTTP_200_OK)
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
        body = 'M?? h??? s?? {0} ???? ???????c ti???p nh???n th??nh c??ng.'.format(record.code)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"H??? s?? {record.code} ???? ???????c ti???p nh???n",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "D???ch v??? c??ng Epoch Making xin th??ng b??o"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('Ti???p nh???n h??? s?? {0} th??nh c??ng'.format(record.code), status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        record = self.get_object()
        record.status = 4
        record.content = request.data.get("content")
        record.save()
        site = settings.HOST_URL
        url = site + "/" + "tracuuhoso/" + str(record.id)
        body = 'M?? h??? s?? {0} ???? b??? h???y.'.format(record.code)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"H??? s?? {record.code} ???? b??? h???y",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "D???ch v??? c??ng Epoch Making xin th??ng b??o"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('H???y h??? s?? {0} th??nh c??ng'.format(record.code), status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        record = self.get_object()
        # if record.approve.user_assignment.id != request.user:
        #     return Response("User n??y kh??ng ???????c ch??? ?????nh cho h??? s?? {0}".format(record.code), status=status.HTTP_200_OK)
        if record.status == 1:
            return Response("H??? s?? {0} ch??a ???????c ti???p nh???n".format(record.code), status=status.HTTP_200_OK)
        if record.status == 4:
            return Response("H??? s?? {0} ???? b??? h???y".format(record.code), status=status.HTTP_200_OK)
        if record.status == 0:
            return Response("H??? s?? {0} ch??a thanh to??n".format(record.code), status=status.HTTP_200_OK)
        record.status = 3
        record.content = request.data.get("content")
        record.save()
        site = settings.HOST_URL
        url = site + "/" + "tracuuhoso/" + str(record.id)
        body = 'M?? h??? s?? {0} ???????c duy???t th??nh c??ng v?? s??? s???m ???????c g???i ?????n ?????a ch??? {1}.'.format(record.service.name,
                                                                                               record.address)
        SendSms.send_sms(phone_number=record.phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": f"H??? s?? {record.code} ???????c duy???t",
            "context": {
                "name": record.name_sender,
                "body": body,
                "link": url,
                "title": "D???ch v??? c??ng Epoch Making xin th??ng b??o"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        return Response('Duy???t h??? s?? {0} th??nh c??ng'.format(record.code), status=status.HTTP_200_OK)

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
