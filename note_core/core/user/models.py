from __future__ import annotations

import typing

import pytz
from django.conf import settings  # noqa
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from note_core.core.user.managers import UserManager
from note_core.utilities.django.models import DjangoModelCleanMixin

tzone = pytz.timezone(settings.TIME_ZONE)


class User(DjangoModelCleanMixin, AbstractUser):
    """ User Model
    Primary user model, whereby every
    user in will have a record in user table.
        is_superuser: bool field
        is_staff: bool field (If true user can access admin pages)
    """

    EN = "en"
    AR = "ar"
    LANGUAGE_CHOICES = (
        (EN, _("English")),
        (AR, _("Arabic")),
    )
    email = models.EmailField(_("email address"), unique=True, blank=False, null=False)
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    language = models.CharField(
        _("Language"), choices=LANGUAGE_CHOICES, default=EN, max_length=5
    )
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: typing.List[typing.Any] = []

    class Meta:
        verbose_name_plural = _("Users")

    @property
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> typing.Text:
        return f"{self.email}"

    def __unicode__(self) -> typing.Text:
        return self.__str__()
