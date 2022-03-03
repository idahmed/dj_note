from __future__ import annotations

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)
from rest_framework.test import APIClient

from tests.core.user.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> settings.AUTH_USER_MODEL:
    return UserFactory()


@pytest.fixture
def super_user() -> settings.AUTH_USER_MODEL:
    return UserFactory(superuser=True)


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """
    Fail on unmocked network calls
    """

    def mockreturn(self, method, url, *args, **kwargs):
        raise RuntimeError(
            f"The test was about to {method} {self.scheme}://{self.host}{url}"
        )

    monkeypatch.setattr("urllib3.connectionpool.HTTPConnectionPool.urlopen", mockreturn)


@pytest.fixture(autouse=True)
def no_celery_tasks(monkeypatch):
    """
    Fail on unmocked celery tasks calls
    """

    def mockreturn(name, **options):
        msg = f"This celery task hasn't been mocked: {name}"
        try:
            module_name = name.rsplit(".", 1)[0]
            exec("import " + module_name)
            p = eval(name).__class__.__name__
            if p != "MagicMock":
                raise RuntimeError(msg)
            eval(name + "(**options)")
        except:
            raise RuntimeError(msg)

    monkeypatch.setattr("celery.current_app.send_task", mockreturn)


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # load modules data
        # call_command("loaddata", "fixtures/some fixtures file")

        yield
        # Destroy fixtures
        get_user_model().objects.all().delete()


@pytest.fixture(autouse=True)
def mute_signals(request):
    # Skip applying, if marked with `enabled_signals`
    if "enable_signals" in request.keywords:
        return

    signals = [pre_save, post_save, pre_delete, post_delete, m2m_changed]
    restore = {}
    for signal in signals:
        # Temporally remove the signal's receivers (a.k.a attached functions)
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals():
        # When the test tears down, restore the signals.
        for signal, receivers in restore.items():
            signal.receivers = receivers

    # Called after a test has finished.
    request.addfinalizer(restore_signals)
