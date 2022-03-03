from __future__ import annotations

import logging
import uuid

from django.contrib.auth.models import UserManager as BaseUserManager

from note_core.utilities.django.managers import GetOrRaiseBaseModelManager

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager, GetOrRaiseBaseModelManager):
    def create(self, *args, **kwargs):
        if "username" not in kwargs:
            kwargs["username"] = uuid.uuid4().__str__()
        return super().create(*args, **kwargs)

    def create_superuser(self, email=None, password=None, **extra_fields):
        username = uuid.uuid4().__str__()
        return super(UserManager, self).create_superuser(
            username=username, email=email, password=password, **extra_fields
        )

    def create_user(self, email=None, password=None, **extra_fields):
        username = uuid.uuid4().__str__()
        return super(UserManager, self).create_user(
            username=username, email=email, password=password, **extra_fields
        )
