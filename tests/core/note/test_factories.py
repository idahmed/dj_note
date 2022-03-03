import pytest

from tests.core.note.factories import NoteFactory


@pytest.mark.django_db
def test_note_factory():
    note = NoteFactory()
    assert note.id
    assert note.title
    assert note.content
