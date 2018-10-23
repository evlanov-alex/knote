from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from knoteserver.apps.notes.models import Note, NoteAccess
from knoteserver.apps.profiles.models import Profile
from knoteserver.apps.profiles.serializers import ProfileSerializer


class NoteAccessSerializer(serializers.ModelSerializer):
    note = serializers.IntegerField()

    class Meta:
        model = NoteAccess
        exclude = ('id', )


class NoteSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tags = TagListSerializerField(required=False)
    allowed_users = serializers.ListSerializer(child=serializers.CharField(), required=False)

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'text', 'tags', 'allowed_users')

    def validate_allowed_users(self):
        pass

    def create(self, validated_data):
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)

        note = Note.objects.create(
            author=profile,
            title=validated_data['title'],
            text=validated_data['text']
        )

        note.tags.add(*validated_data.get('tags', []))
