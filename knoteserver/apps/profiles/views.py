from rest_framework import viewsets, mixins

from knoteserver.apps.profiles.models import Profile
from knoteserver.apps.profiles.permissions import ProfilePermission
from knoteserver.apps.profiles.serializers import ProfileSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    permission_classes = (ProfilePermission,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'

    def perform_destroy(self, instance):
        instance.user.delete()
