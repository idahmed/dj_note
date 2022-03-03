from __future__ import annotations

import typing

from django.db import models
from django.utils.translation import gettext_lazy as _

from note_core.core.user.models import User


class Note(models.Model):
    """ Note model to represent notes in app.
    """

    class Visibility(models.TextChoices):
        VISIBLE = "Visible", _("Visible")
        HIDDEN = "Hidden", _("Hidden")
        ARCHIVED = "Archived", _("Archived")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    title = models.CharField(
        max_length=250, null=False, blank=False, help_text="Note title"
    )
    content = models.TextField(help_text="Note content")
    visibility = models.CharField(
        choices=Visibility.choices, max_length=100, default=Visibility.VISIBLE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Notes")

    def __str__(self) -> typing.Text:
        return f"{self.title}"

    def __unicode__(self) -> typing.Text:
        return self.__str__()
