from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from knoteserver.apps.notes.models import Note, NoteAccess
from knoteserver.apps.profiles.models import Profile

UserModel = get_user_model()


class NotesTests(APITestCase):
    def setUp(self):
        password = 'qwerty11'
        username_1 = 'main'
        username_2 = 'test'
        UserModel.objects.create(username=username_1, password=password)
        UserModel.objects.create(username=username_2, password=password)

        self.auth_profile = Profile.objects.get(user__username=username_1)
        self.other_profile = Profile.objects.get(user__username=username_2)

        self.token = Token.objects.create(user=self.auth_profile.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token.key))

        self.anon_client = APIClient()

        # POPULATE DATABASE
        # 3 for auth profile, 2 for another
        # 3 with tag 'pupa', 4 with tag 'lupa', 2 with both tags
        self.counts = {
            'notes_for_auth_profile': 3,
            'notes_for_another': 2,
            'pupa_tag': 3,
            'lupa_tag': 4,
            'both_tags': 2
        }

        note = Note.objects.create(author=self.auth_profile, text='text')
        note.tags.add('pupa', 'lupa')

        note = Note.objects.create(author=self.auth_profile, text='text')
        note.tags.add('pupa')

        note = Note.objects.create(author=self.auth_profile, text='text')
        note.tags.add('lupa')

        note = Note.objects.create(author=self.other_profile, text='text')
        note.tags.add('pupa', 'lupa')
        NoteAccess.objects.create(note=note, profile=self.auth_profile, can_write=False)

        note = Note.objects.create(author=self.other_profile, text='text')
        note.tags.add('lupa')
        NoteAccess.objects.create(note=note, profile=self.auth_profile, can_write=True)

    def test_unauthorized_request(self):
        url = reverse('notes:note-list')
        response = self.anon_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_endpoint(self):
        url = reverse('notes:note-list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test tags parameter
        response = self.client.get(url, {'tags': 'pupa, lupa'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(url, {'tags': 'pupa'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url, {'tags': 'a' * 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

        # test username parameter
        response = self.client.get(url, {'username': self.other_profile.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(url, {'username': 'a' * 30})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test ordering parameter
        # to be continued...

    def test_retrieve_endpoint(self):
        """To be implemented."""
