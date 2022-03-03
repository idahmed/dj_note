from django.db import models


class DjangoModelCleanMixin(models.Model):
    """ DjangoModelCleanMixin will run full clean on every save operation
    which enforces validation check on new object creations
    """

    class Meta:
        abstract = True

    def save(self, **kwargs):
        self.full_clean()
        return super().save(**kwargs)
