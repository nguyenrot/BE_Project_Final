from rest_framework import viewsets
from api_files.serializers import (
    ReceptionRecordSerializer,
    ReceptionRecordDetailSerializer,
    ViewCustomerRecordSerializer
)
from api_files.models import ReceptionRecord
from rest_framework.response import Response
from rest_framework import status
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
import random
import string
from api_base.services import SendSms, SendMail


class RecordView(viewsets.ModelViewSet):
    queryset = ReceptionRecord.objects.all()

    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"], ["employee_receive"], ["employee_approve"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
    }

    class MyList(list):
        def get(self, index, default=None):
            return self[index] if len(self) > index else default

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = [TokenHasActionScope]
        if self.action in ("retrieve", "list", "create"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ("retrieve"):
            return ViewCustomerRecordSerializer
        return ReceptionRecordSerializer

    def create(self, request, *args, **kwargs):
        name_sender = request.data.get("name_sender")
        phone_number = request.data.get("phone_number")
        address = request.data.get("address")
        email = request.data.get("email")
        file = request.data.get("file")
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data_record = {"name_sender": name_sender, "phone_number": phone_number, "address": address, "file": file,
                       "code": code, "email": email}
        record_serializer = ReceptionRecordSerializer(data=data_record)
        if not record_serializer.is_valid():
            return Response(record_serializer.errors)
        record_serializer.save()
        id_record = record_serializer.data.get("id")
        attach = self.MyList(request.data.getlist('attach'))
        file_detail = self.MyList(request.data.getlist('file_detail'))
        for i in range(len(file_detail)):
            data = {'reception_record': id_record, "attach": attach.get(i), "file_detail": file_detail.get(i)}
            record_detail_serializer = ReceptionRecordDetailSerializer(data=data)
            if record_detail_serializer.is_valid():
                record_detail_serializer.save()
            else:
                return Response(record_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        record = ReceptionRecord.objects.get(pk=id_record)
        body = 'Bạn đã nộp hồ sơ {0} thành công.Mã hồ sơ của bạn là {1}'.format(record.file.name, record.code)
        SendSms.send_sms(phone_number=phone_number, body=body)
        mail_data = {
            "template": "mail_templates/mail_successful_file_registration.html",
            "subject": "Đăng ký hồ sơ thành công",
            "context": {
                "name": record.name_sender,
                "body": body,
                "title": "Dịch vụ công Epoch Making xin thông báo"
            },
            "to": [record.email],
        }
        SendMail.send_html_email(mail_data)
        view_record_serializer = ViewCustomerRecordSerializer(record)
        return Response(view_record_serializer.data, status=status.HTTP_201_CREATED)
