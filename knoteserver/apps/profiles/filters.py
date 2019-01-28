from django_filters import rest_framework as filters
from django.db.models import Value
from django.db.models.functions import StrIndex

from knoteserver.apps.profiles.models import Profile


class ProfilesFilterSet(filters.FilterSet):
    """FilterSet for profile API views."""

    search = filters.CharFilter(method='search_by_username')

    class Meta:  # noqa: Z306, D106
        model = Profile
        fields = ()

    def search_by_username(self, queryset, name, expr):
        """First starting with expr, then containing expr."""
        queryset = queryset.annotate(
            expr_position=StrIndex('user__username', Value(expr)),
        ).filter(
            expr_position__gt=0,
        ).order_by(
            'expr_position',
            'user__username',
        )

        return queryset
