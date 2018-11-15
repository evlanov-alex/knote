from django_filters import rest_framework as filters

from knoteserver.apps.notes.models import Note


EMPTY_VALUES = (None, '', [], (), {})


class NotesFilterSet(filters.FilterSet):
    tags = filters.CharFilter(method='filter_by_tags')
    username = filters.CharFilter(method='filter_by_username')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created'),
            ('updated_at', 'updated'),
        )
    )

    class Meta:
        model = Note
        fields = ()

    def filter_by_tags(self, queryset, name, value):
        if value in EMPTY_VALUES:
            return queryset

        tags = value.split(',')
        for tag in tags:
            queryset = queryset.filter(tags__name=tag.strip())

        return queryset

    def filter_by_username(self, queryset, name, value):
        if value in EMPTY_VALUES or value == self.request.user.username:
            return queryset.filter(author__user=self.request.user)

        return queryset.filter(author__user__username=value).filter(allowed_profiles__user=self.request.user)
