from rest_framework import permissions


class IsClientOwnerOrReadOnly(permissions.BasePermission):
    """Anyone can browse the menu; only the owning client can edit their own items."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'client')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.client.user_id == request.user.id
