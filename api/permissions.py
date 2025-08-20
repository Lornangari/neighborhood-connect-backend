from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only comment owners to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # Safe methods like GET are allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.user == request.user


# events
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
