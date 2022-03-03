from __future__ import annotations

import logging

from django.db import models

logger = logging.getLogger(__name__)


class NoteManager(models.Manager):
    pass
