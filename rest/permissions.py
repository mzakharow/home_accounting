from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and obj.user == request.user
        )

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)