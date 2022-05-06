from rest_framework import viewsets
from api_oauth2.permissions.oauth2_permissions import TokenHasActionScope
from api_evaluates.serializers import EvaluateSerializer, EvaluateCreateSerializer
from api_evaluates.models import Evaluate
from rest_framework.response import Response
from rest_framework import status
from api_files.models import ReceptionRecord
from rest_framework.decorators import action


class EvaluateView(viewsets.ModelViewSet):
    # queryset = Evaluate.objects.all()
    # serializer_class = EvaluateSerializer

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
        if self.action in ("retrieve", "list", "create", "statistic"):
            self.permission_classes = []
        return super(self.__class__, self).get_permissions()

    def get_serializer_class(self):
        if self.action in ("create"):
            return EvaluateCreateSerializer
        return EvaluateSerializer

    def get_queryset(self):
        if self.action in ("create"):
            return None
        return Evaluate.objects.all()

    def create(self, request, *args, **kwargs):
        code = request.data.get("code")
        question_1 = request.data.get("question_1")
        question_2 = request.data.get("question_2")
        question_3 = request.data.get("question_3")
        question_4 = request.data.get("question_4")
        question_5 = request.data.get("question_5")
        record = ReceptionRecord.objects.filter(code=code).first()

        if not record:
            return Response("Không tìm thấy mã hồ sơ", status=status.HTTP_400_BAD_REQUEST)

        data = {
            "record": record.id,
            "question_1": question_1,
            "question_2": question_2,
            "question_3": question_3,
            "question_4": question_4,
            "question_5": question_5,
        }
        serializer = EvaluateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Đã gửi đánh giá", status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def statistic(self, request):

        dict_question_1 = {
            1: 0,
            2: 0,
            3: 0
        }
        dict_question_2 = {
            1: 0,
            2: 0,
            3: 0
        }
        dict_question_3 = {
            1: 0,
            2: 0,
            3: 0
        }
        dict_question_4 = {
            1: 0,
            2: 0,
            3: 0
        }
        dict_question_5 = {
            1: 0,
            2: 0,
            3: 0
        }

        queryset = Evaluate.objects.all()
        for evaluate in queryset:

            quantity_q_1, quantity_q_2, quantity_q_3, quantity_q_4, quantity_q_5 = 0, 0, 0, 0, 0
            if evaluate.question_1 == 1:
                quantity_q_1 += 1
            elif evaluate.question_1 == 2:
                quantity_q_2 += 1
            elif evaluate.question_1 == 3:
                quantity_q_3 += 1
            dict_question_1[1] = dict_question_1[1] + quantity_q_1
            dict_question_1[2] = dict_question_1[2] + quantity_q_2
            dict_question_1[3] = dict_question_1[3] + quantity_q_3
            print(dict_question_1)

            quantity_q_1, quantity_q_2, quantity_q_3, quantity_q_4, quantity_q_5 = 0, 0, 0, 0, 0
            if evaluate.question_2 == 1:
                quantity_q_1 += 1
            elif evaluate.question_2 == 2:
                quantity_q_2 += 1
            elif evaluate.question_2 == 3:
                quantity_q_3 += 1
            dict_question_2[1] = dict_question_2[1] + quantity_q_1
            dict_question_2[2] = dict_question_2[2] + quantity_q_2
            dict_question_2[3] = dict_question_2[3] + quantity_q_3

            quantity_q_1, quantity_q_2, quantity_q_3, quantity_q_4, quantity_q_5 = 0, 0, 0, 0, 0
            if evaluate.question_3 == 1:
                quantity_q_1 += 1
            elif evaluate.question_3 == 2:
                quantity_q_2 += 1
            elif evaluate.question_3 == 3:
                quantity_q_3 += 1
            dict_question_3[1] = dict_question_3[1] + quantity_q_1
            dict_question_3[2] = dict_question_3[2] + quantity_q_2
            dict_question_3[3] = dict_question_3[3] + quantity_q_3

            quantity_q_1, quantity_q_2, quantity_q_3, quantity_q_4, quantity_q_5 = 0, 0, 0, 0, 0
            if evaluate.question_4 == 1:
                quantity_q_1 += 1
            elif evaluate.question_4 == 2:
                quantity_q_2 += 1
            elif evaluate.question_4 == 3:
                quantity_q_3 += 1
            dict_question_4[1] = dict_question_4[1] + quantity_q_1
            dict_question_4[2] = dict_question_4[2] + quantity_q_2
            dict_question_4[3] = dict_question_4[3] + quantity_q_3

            quantity_q_1, quantity_q_2, quantity_q_3, quantity_q_4, quantity_q_5 = 0, 0, 0, 0, 0
            if evaluate.question_5 == 1:
                quantity_q_1 += 1
            elif evaluate.question_5 == 2:
                quantity_q_2 += 1
            elif evaluate.question_5 == 3:
                quantity_q_3 += 1
            dict_question_5[1] = dict_question_5[1] + quantity_q_1
            dict_question_5[2] = dict_question_5[2] + quantity_q_2
            dict_question_5[3] = dict_question_5[3] + quantity_q_3
        list_question = [dict_question_1, dict_question_2, dict_question_3, dict_question_4, dict_question_5]
        return Response({"total_evaluate": queryset.count(), "results": list_question})
