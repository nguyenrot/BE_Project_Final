from common.constants.base_const import Const

__all__ = ["Scope"]


class Scope(Const):
    GROUP_SCOPE = {
        "user": "User",
        "admin": "User",
        "role": "Role",
        "contract": "Contract",
        "office": "Office",
        "employee": "Employee",
        "template": "Template",
        "payroll": "Payroll",
        "payroll-schema": "Payroll Schema",
    }
