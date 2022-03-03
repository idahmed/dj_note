import logging
import typing

logger = logging.getLogger(__name__)


class DjangoAdminDisableCreateMixin(object):
    """DjangoAdminDisableCreateMixin prevents create actions from django admin"""

    def has_add_permission(self, *args, **kwargs) -> bool:
        return False


class DjangoAdminDisableDeleteMixin(object):
    """DjangoAdminDisableDeleteMixin prevents delete actions from django admin"""

    def has_delete_permission(self, *args, **kwargs) -> bool:
        return False


class DjangoAdminDisableUpdateMixin(object):
    """DjangoAdminDisableUpdateMixin prevents update actions from django admin"""

    def get_readonly_fields(self, request, obj=None) -> typing.List:
        return [field.name for field in self.model._meta.fields]


class DjangoAdminReadOnlyMixin(
    DjangoAdminDisableCreateMixin,
    DjangoAdminDisableDeleteMixin,
    DjangoAdminDisableUpdateMixin,
):
    """ DjangoAdminReadOnlyMixin prevents CRUD actions from django admin
    """
