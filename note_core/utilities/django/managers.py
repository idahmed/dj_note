from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class GetOrRaiseBaseModelManager(models.Manager):
    def get_or_raise(self, error_msg, **lookup):
        try:
            return self.get(**lookup)
        except ObjectDoesNotExist:
            raise Http404(error_msg)
