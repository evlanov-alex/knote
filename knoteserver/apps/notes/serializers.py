from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from knoteserver.apps.notes.models import Note
from knoteserver.apps.profiles.serializers import ProfileSerializer


class NoteSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'text', 'tags')
