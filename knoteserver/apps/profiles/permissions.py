from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProfilePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            (request.method in SAFE_METHODS) or
            (request.user and request.user.is_authenticated and request.user == obj.user)
        )
