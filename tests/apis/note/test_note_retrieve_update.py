import pytest
from django.urls import reverse
from rest_framework import status

from note_core.core.note.models import Note
from tests.core.note.factories import NoteFactory


@pytest.mark.django_db
def test_retrieve_updating_note(api_client, user):

    note = NoteFactory(user=user)
    api_client.force_authenticate(user)

    # Test retrieve
    response = api_client.get(reverse("note:note-detail", args=[note.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == note.title

    # Test update
    response = api_client.patch(
        reverse("note:note-detail", args=[note.id]), data={"title": "updated"}
    )
    assert response.status_code == status.HTTP_200_OK
    note.refresh_from_db()
    assert response.json()["title"] == "updated" == note.title

    # Test permissions
    note_ = NoteFactory()
    assert Note.objects.count() == 2
    response = api_client.get(reverse("note:note-detail", args=[note_.id]))
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Test delete
    response = api_client.delete(reverse("note:note-detail", args=[note.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Note.objects.count() == 1
