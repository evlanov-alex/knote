from rest_framework.permissions import BasePermission, SAFE_METHODS


class NotePermission(BasePermission):


    def has_object_permission(self, request, view, obj):
        return True
        # return (
        #     request.method in SAFE_METHODS and
        #     request.user and request.user.is_authenticated and
        #     request.user == obj.author.user
        # )