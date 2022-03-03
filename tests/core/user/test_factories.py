import pytest

from tests.core.user.factories import UserFactory


@pytest.mark.django_db
def test_user_factory():
    user = UserFactory()
    assert user.id
    assert not user.is_staff and not user.is_superuser
    assert user.__str__()


@pytest.mark.django_db
def test_super_user_factory():
    super_user = UserFactory(superuser=True)
    assert super_user.id
    assert super_user.is_staff
    assert super_user.is_superuser
    assert super_user.__str__()


@pytest.mark.django_db
def test_staff_user_factory():
    # TODO: Is there a better way to handle post generated test data with factory.Traits?
    instance = UserFactory(staff=True)
    assert instance.id
    assert instance.is_staff
    assert not instance.is_superuser
    assert instance.__str__()
