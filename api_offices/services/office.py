from api_offices.models import Office, Group


class OfficeService:
    @classmethod
    def get_tree(cls, group, parent=False):
        if not group.parent_group:
            child_offices = list(cls.get_office_query_set(group.id))
            if not parent:
                return child_offices
            else:
                for child in child_offices:
                    child["office_childs"] = list(cls.get_office_child_query_set(child.get("id")))
                return child_offices
        else:
            return cls.get_tree(group.parent_group, True)

    @classmethod
    def get_office_query_set(cls, group_id):
        return Office.objects.filter(group=group_id).values("id", "nanme", "description")

    @classmethod
    def get_office_child_query_set(cls, office_id):
        return Office.objects.filter(parent_office=office_id).values("id", "nanme", "description")
