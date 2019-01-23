from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProfilePermission(BasePermission):
    """Permissons for profile API endpoints."""

    def has_permission(self, request, view):
        """Only authenticated user."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, profile_obj):
        """Read access or full access if you are owner."""
        return request.method in SAFE_METHODS or request.user == profile_obj.user
