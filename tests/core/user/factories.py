from __future__ import annotations

import random
import string

import factory
from django.db.models import signals
from factory import Faker

from note_core.core.user.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = factory.Sequence(lambda n: f"email_{n}@1fort.com")

    # TODO: add business subfactory
    # business = factory.SubFactory(BusinessFactory)

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
        signals.post_save.disconnect(
            sender=User, dispatch_uid="create_acronis_tenant_member"
        )
        signals.post_save.disconnect(sender=User, dispatch_uid="send_welcoming_email")
        manager = cls._get_manager(target_class)
        return manager.create_user(*args, **kwargs)
