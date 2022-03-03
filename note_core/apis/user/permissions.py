from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class UserPermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.user.is_anonymous and request.method in [
            "POST",
        ]:
            return True
        if request.user.is_authenticated and request.method in [
            "GET",
            "PATCH",
        ]:
            return True
        return False
