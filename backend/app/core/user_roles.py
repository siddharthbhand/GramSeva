from enum import Enum


class UserRole(str, Enum):
    CITIZEN = "citizen"
    OFFICER = "officer"
    DEPARTMENT_HEAD = "department_head"
    ADMIN = "admin"