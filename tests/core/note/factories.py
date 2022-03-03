from __future__ import annotations

import random

import factory
from factory import Faker

from note_core.core.note.models import Note
from tests.core.user.factories import UserFactory


class NoteFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    title = Faker("sentence", nb_words=2)
    content = Faker("sentence", nb_words=int(random.randint(0, 10)))

    class Meta:
        model = Note

    def __new__(cls, *args, **kwargs) -> NoteFactory.Meta.model:
        return super().__new__(*args, **kwargs)

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create(*args, **kwargs)
