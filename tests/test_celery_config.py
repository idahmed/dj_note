import pytest


@pytest.mark.integration
@pytest.mark.django_db(transaction=True)
def test_live_worker(celery_app, celery_worker):
    @celery_app.task
    def mul(x, y):
        return x * y

    celery_worker.reload()

    assert mul.delay(4, 4).get(timeout=10) == 16
