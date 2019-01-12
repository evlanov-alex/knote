from rest_framework.permissions import BasePermission


class NotePermission(BasePermission):
    """Permission class for controlling access for Notes."""

    read_methods = {'GET', 'HEAD', 'OPTIONS'}
    write_methods = {'PUT', 'PATCH'}  # without DELETE method, its allowed only for owner

    def has_permission(self, request, view):
        """Has permission only if user authenticated."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, note):
        """Check if current authenticated has any permissions for notes objects."""
        if note.author.user == request.user:
            return True

        if note.allowed_profiles.filter(user=request.user).exists():
            if request.method in self.read_methods:
                return True

            if request.method in self.write_methods:
                access = note.access.get(profile__user=request.user)
                return access.can_write

        return False
