from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins

from knoteserver.apps.notes.models import Note
from knoteserver.apps.notes.filters import NotesFilterSet
from knoteserver.apps.notes.permissions import NotePermission
from knoteserver.apps.notes.serializers import NoteSerializer


class NoteViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    permission_classes = (NotePermission,)
    serializer_class = NoteSerializer
    filter_class = NotesFilterSet
    queryset = Note.objects\
        .select_related('author', 'author__user')\
        .prefetch_related('access', 'tags')\
        .order_by('-created_at')

    def get_object(self):
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    # изменять текст заметки может только владелец и кому доступна заметка
    # изменять название заметки может только владелец
    # удалять заметку может только владелец
    # grant_access
    # remove_access
