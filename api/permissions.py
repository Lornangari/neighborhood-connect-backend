from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only comment owners to edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.user == request.user


# help-post
class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read for authenticated users.
    Allow write (PUT/DELETE/PATCH) only if request.user is the object's owner or is_staff.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return getattr(obj, 'user', None) == request.user or request.user.is_staff






# events
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'
