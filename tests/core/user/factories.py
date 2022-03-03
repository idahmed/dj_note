from __future__ import annotations

import random
import string

import factory
from factory import Faker

from note_core.core.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = factory.Sequence(lambda n: f"email_{n}@note.com")

    password = "".join(random.choice(string.ascii_lowercase) for i in range(20))

    class Meta:
        model = User

    class Params:
        superuser = factory.Trait(is_staff=True, is_superuser=True)
        staff = factory.Trait(is_staff=True,)

    def __new__(cls, *args, **kwargs) -> UserFactory.Meta.model:
        return super().__new__(*args, **kwargs)

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        manager = cls._get_manager(target_class)
        return manager.create_user(*args, **kwargs)
