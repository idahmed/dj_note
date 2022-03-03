import pytest
from django.urls import reverse
from rest_framework import status

from note_core.core.note.models import Note
from tests.core.note.factories import NoteFactory


@pytest.mark.django_db
def test_list_create_note(api_client, user):

    api_client.force_authenticate(user)
    data = {"title": "test title", "content": "some random test content"}

    # Test create
    response = api_client.post(reverse("note:note-list"), data,)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == data["title"]
    assert Note.objects.count() == 1

    # Test list
    response = api_client.get(reverse("note:note-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == Note.objects.count() == 1
    assert response.json()["results"][0]["title"] == data["title"]

    # permissions
    NoteFactory()
    assert Note.objects.count() == 2
    response = api_client.get(reverse("note:note-list"))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["count"] == 1
