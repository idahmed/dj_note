from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NoteConfig(AppConfig):
    name = "note_core.core.note"
    verbose_name = _("notes")
