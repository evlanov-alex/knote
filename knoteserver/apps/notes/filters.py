from django_filters import rest_framework as filters

from knoteserver.apps.notes.models import Note


class TagsFilter(filters.Filter):
    def filter(self, qs, value):
        if value in self.field.empty_values:
            return qs

        tags = value.split(',')
        for tag in tags:
            qs = qs.filter(tags__name=tag.strip())

        return qs


class NotesFilterSet(filters.FilterSet):
    tags = TagsFilter(field_name='tags')
    username = filters.CharFilter(field_name='author__user__username', lookup_expr='exact')
    profile_id = filters.NumberFilter(field_name='author__id')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created'),
            ('updated_at', 'updated'),
        )
    )

    class Meta:
        model = Note
        fields = ()
