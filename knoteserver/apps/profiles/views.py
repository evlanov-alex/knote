from rest_framework import viewsets, mixins, permissions, generics

from knoteserver.apps.profiles.models import Profile
from knoteserver.apps.profiles.permissions import ProfilePermission
from knoteserver.apps.profiles.serializers import ProfileSerializer


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """API viewset for profiles."""

    permission_classes = (ProfilePermission,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'

    def perform_destroy(self, instance):  # noqa: D102
        instance.user.delete()


class CurrentUserAPIView(generics.RetrieveAPIView):
    """API view for returning currently authenticated user."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):  # noqa: D102
        profile = Profile.objects.select_related('user').get(user=self.request.user)
        return profile
