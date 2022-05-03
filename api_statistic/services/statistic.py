from api_services.models import Service
from api_files.models import ReceptionRecord
from datetime import datetime


class StatisticService:
    @classmethod
    def service_record_number(cls, time_start=None, time_end=None, status=None):
        time_start_date = datetime.strptime(time_start, '%Y-%m-%d') if time_start else None
        time_end_date = datetime.strptime(time_end, '%Y-%m-%d') if time_end else None
        lts = list()
        total_all = 0
        display_status = None
        if status:
            for choice in ReceptionRecord.STATUS_CHOICES:
                if choice[0] == int(status):
                    display_status = choice[1]
                    break
        list_services = Service.objects.all()
        for service in list_services:
            services = service.reception
            if time_start_date and time_end_date:
                services = services.filter(created_at__gte=time_start_date, created_at__lte=time_end_date)
            if time_start_date and not time_end_date:
                services = services.filter(created_at__gte=time_start_date)
            if not time_start_date and time_end_date:
                services = services.filter(created_at__lte=time_end_date)
            if status:
                services = services.filter(status=status)
            if any([time_start_date, time_end_date, status]):
                services = services.all()
            dict_service = dict()
            dict_service["id"] = service.id
            dict_service["name"] = service.name
            dict_service["id_field"] = service.field.id
            dict_service["name_field"] = service.field.name
            dict_service["id_office"] = service.field.office.id
            dict_service["name_office"] = service.field.office.name
            dict_service["number_record"] = services.count()
            dict_service["total_amount"] = dict_service["number_record"] * service.amount
            total_all += dict_service["total_amount"]
            lts.append(dict_service)
        return {"total_records": total_all, "total_serices": list_services.count(), "status": status,
                "display_status": display_status,
                "time_start": time_start,
                "time_end": time_end,
                "results": sorted(lts, key=lambda x: x['total_amount'], reverse=True)}

    @classmethod
    def service(cls, time_start=None, time_end=None, status=None, service=None):
        time_start_date = datetime.strptime(time_start, '%Y-%m-%d') if time_start else None
        time_end_date = datetime.strptime(time_end, '%Y-%m-%d') if time_end else None
        lst = list()
        records = service.reception
        display_status = None
        if time_start_date and time_end_date:
            records = records.filter(created_at__gte=time_start_date, created_at__lte=time_end_date)
        if time_start_date and not time_end_date:
            records = records.filter(created_at__gte=time_start_date)
        if not time_start_date and time_end_date:
            records = records.filter(created_at__lte=time_end_date)
        if status:
            records = records.filter(status=status)
            for choice in ReceptionRecord.STATUS_CHOICES:
                if choice[0] == int(status):
                    display_status = choice[1]
                    break
        if not any([time_start_date, time_end_date, status]):
            records = records.all()
        total_records = 0
        for record in records:
            dict_record = dict()
            dict_record["id"] = record.id
            dict_record["name_sender"] = record.name_sender
            dict_record["code"] = record.code
            dict_record["status"] = record.status
            dict_record["display_status"] = record.get_status_display()
            total_records += 1
            lst.append(dict_record)
        return {"id": service.id, "name": service.name, "amount": service.amount,
                "total_amount": service.amount * total_records,
                "status": status, "display_status": display_status,
                "time_start": time_start,
                "time_end": time_end, "total_records": total_records, "records": lst}
