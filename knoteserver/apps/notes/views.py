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

    # изменять текст заметки может только владелец и кому доступна заметка
    # изменять название заметки может только владелец
    # удалять заметку может только владелец
    # grant_access
    # remove_access
