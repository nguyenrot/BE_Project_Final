from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from api_statistic.services import StatisticService
from api_services.models import Service
from django.shortcuts import get_object_or_404


class StatisticView(viewsets.ViewSet):
    required_alternate_scopes = {
        "list": [["admin"], ["super_admin"]],
        "create": [["admin"], ["super_admin"]],
        "retrieve": [["admin"], ["super_admin"]],
        "update": [["admin"], ["super_admin"]],
        "partial_update": [["admin"], ["super_admin"]],
        "destroy": [["admin"], ["super_admin"]],
        "service_record_number": [["admin"], ["super_admin"]],
        "service": [["admin"], ["super_admin"]],
    }

    @action(methods=['GET'], detail=False)
    def service_record_number(self, request):
        time_start = request.GET.get("time_start")
        time_end = request.GET.get("time_end")
        status = request.GET.get("status")
        data = StatisticService.service_record_number(time_start, time_end, status)
        return Response(data)

    @action(methods=['GET'], detail=True)
    def get(self, request, pk=None):
        service = get_object_or_404(Service,pk=pk)
        time_start = request.GET.get("time_start")
        time_end = request.GET.get("time_end")
        status = request.GET.get("status")
        data = StatisticService.service(time_start, time_end, status,service)
        return Response(data)
