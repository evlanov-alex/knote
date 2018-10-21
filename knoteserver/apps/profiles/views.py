from rest_framework import viewsets

from knoteserver.apps.profiles.models import Profile
from knoteserver.apps.profiles.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.select_related('user')
    lookup_url_kwarg = 'username'
    lookup_field = 'user__username'
