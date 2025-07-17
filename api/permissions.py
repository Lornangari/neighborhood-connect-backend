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
