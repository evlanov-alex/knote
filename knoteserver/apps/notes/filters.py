from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters

from knoteserver.apps.notes.models import Note

EMPTY_VALUES = (None, '', [], (), {})


class NotesFilterSet(filters.FilterSet):
    """FilterSet for notes view."""

    tags = filters.CharFilter(method='filter_by_tags')
    username = filters.CharFilter(method='filter_by_username')
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created'),
            ('updated_at', 'updated'),
        ),
    )

    def filter_queryset(self, queryset):
        """Filter out empty usernames."""
        # handling username empty value here cause of filter_by_username wont be called when value is empty
        username_value = self.form.cleaned_data['username']
        if username_value in EMPTY_VALUES:
            queryset = queryset.filter(author__user=self.request.user)

        return super(NotesFilterSet, self).filter_queryset(queryset)

    class Meta:  # noqa: Z306,D106
        model = Note
        fields = ()

    def filter_by_tags(self, queryset, name, tags):
        """Filter notes by tags."""
        if tags in EMPTY_VALUES:
            return queryset

        tags = tags.split(',')
        for tag in tags:
            queryset = queryset.filter(tags__name=tag.strip())

        return queryset

    def filter_by_username(self, queryset, name, username):
        """Filter notes b username."""
        user = get_object_or_404(User, username=username)

        if user == self.request.user:
            return queryset.filter(author__user=self.request.user)

        return queryset.filter(author__user=user).filter(allowed_profiles__user=self.request.user)
