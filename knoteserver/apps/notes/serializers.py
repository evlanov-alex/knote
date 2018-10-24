from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField

from knoteserver.apps.notes.models import Note, NoteAccess
from knoteserver.apps.profiles.models import Profile
from knoteserver.apps.profiles.serializers import ProfileSerializer


class NoteAccessSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    username = serializers.CharField(write_only=True)

    class Meta:
        model = NoteAccess
        fields = '__all__'
        extra_kwargs = {
            'note': {'write_only': True},
        }

    def create(self, validated_data):
        profile = Profile.objects.get(user__username=validated_data['username'])

        note_access = NoteAccess.objects.create(
            profile=profile,
            note=validated_data['note'],
            can_write=validated_data['can_write'],
        )

        return note_access


class NoteSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    tags = TagListSerializerField(required=False)
    access = NoteAccessSerializer(many=True, required=False)

    class Meta:
        model = Note
        fields = ('id', 'author', 'title', 'text', 'tags', 'access')

    def validate_title(self, title):
        print(title)
        return title

    def validate_access(self, access):
        print(access)
        return access

    def create(self, validated_data):
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)

        note = Note.objects.create(
            author=profile,
            title=validated_data['title'],
            text=validated_data['text']
        )

        note.tags.add(*validated_data.get('tags', []))
        note.access.add(*validated_data.get('access', []))
        return note
