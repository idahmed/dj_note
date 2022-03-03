from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    """
    Permission to oweners only.
    """

    def has_permission(self, request, view):
        return request.user.role == "Owner"


class AdminPermission(permissions.BasePermission):
    """
    Permission to admins only.
    """

    def has_permission(self, request, view):
        return request.user.role in ["Owner", "Admin"]
