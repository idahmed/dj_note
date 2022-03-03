from rest_framework import permissions


class OwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own notes
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj here is a UserProfile instance
        return obj.user == request.user


class AdminPermission(permissions.BasePermission):
    """
    Permission to admins only.
    """

    def has_permission(self, request, view):
        return request.user.role in ["Owner", "Admin"]
