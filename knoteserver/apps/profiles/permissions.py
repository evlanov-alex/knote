from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProfilePermission(BasePermission):
    """Permissons for profile API endpoints."""

    def has_permission(self, request, view):  # noqa: D102
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, profile_obj):  # noqa: D102
        return request.method in SAFE_METHODS or request.user == profile_obj.user
