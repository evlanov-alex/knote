from django.conf import settings
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
        """Create NoteAccess instance for profile with specified name."""
        profile = Profile.objects.get(user__username=validated_data['username'])

        note_access = NoteAccess.objects.create(
            profile=profile,
            note=validated_data['note'],
            can_write=validated_data['can_write'],
        )

        return note_access


class NoteSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    access = NoteAccessSerializer(many=True, read_only=True)
    tags = TagListSerializerField(required=False)

    is_owner = serializers.SerializerMethodField(read_only=True)
    can_write = serializers.SerializerMethodField(read_only=True)

    default_error_messages = {
        'bad_tags': 'Incorrect tags',
    }

    class Meta:
        model = Note
        exclude = ('allowed_profiles',)

    def get_is_owner(self, note: Note) -> bool:
        """Does current user is owner."""
        return self.context['request'].user == note.author.user

    def get_can_write(self, note: Note):
        """Does current user has access for editing."""
        if self.context['request'].user != note.author.user:
            return note.access.get(profile__user=self.context['request'].user).can_write

        return True

    def validate_tags(self, tags):
        """Validate tags that they does not have bad chars."""
        for tag in tags:
            if not settings.TAG_REGEXP.match(tag):
                self.fail('bad_tags')

        return list(tags)

    def create(self, validated_data):
        """Create Note with current user as author."""
        request = self.context.get('request')
        profile = Profile.objects.get(user=request.user)

        note = Note.objects.create(
            author=profile,
            title=validated_data['title'],
            text=validated_data['text'],
        )

        note.tags.add(*validated_data.get('tags', []))
        return note
