from api_offices.models import Office
from api_fields.models import Field
from api_services.models import Service


class Services:
    @classmethod
    def get_services(cls, id_office=None, id_field=None, search=None):
        services = Service.objects.all()

        if len(id_field):
            services = services.filter(field_id=id_field)
        if len(id_office):
            services = services.filter(field__office_id=id_office)
        if len(search):
            services = services.filter(name__icontains=search)
        return services
