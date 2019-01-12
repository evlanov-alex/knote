from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from knoteserver.apps.notes.filters import NotesFilterSet
from knoteserver.apps.notes.models import Note
from knoteserver.apps.notes.permissions import NotePermission
from knoteserver.apps.notes.serializers import NoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    """CRUD ViesSet for Notes."""

    permission_classes = (NotePermission,)
    serializer_class = NoteSerializer
    filter_class = NotesFilterSet
    queryset = Note.objects.select_related(
        'author',
        'author__user',
    ).prefetch_related(
        'access',
        'tags',
    ).order_by(
        '-created_at',
    )

    def get_object(self):
        """Returns the note the view is displaying."""
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (  # noqa: S101
            'Expected view {0} to be called with a URL keyword argument '
            'named "{1}". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.'.format(self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        note = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, note)
        return note

    # изменять текст заметки может только владелец и кому доступна заметка
    # изменять название заметки может только владелец
    # удалять заметку может только владелец
    # grant_access
    # remove_access
