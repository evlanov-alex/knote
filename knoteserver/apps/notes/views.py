from rest_framework import viewsets

from knoteserver.apps.notes.models import Note
from knoteserver.apps.notes.serializers import NoteSerializer


class NoteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.select_related('author', 'author__user')
