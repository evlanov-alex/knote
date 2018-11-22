from rest_framework.permissions import BasePermission


class NotePermission(BasePermission):
    READ_METHODS = {'GET', 'HEAD', 'OPTIONS'}
    WRITE_METHODS = {'PUT', 'PATCH'} # without DELETE method, its allowed only for owner

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.author.user == request.user:
            return True

        if obj.allowed_profiles.filter(user=request.user).exists():
            if request.method in self.READ_METHODS:
                return True

            if request.method in self.WRITE_METHODS:
                access = obj.access.get(profile__user=request.user)
                return access.can_write

        return False
