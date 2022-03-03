import factory
import pytest
from django.urls import reverse
from rest_framework import status

url = reverse("user:user-detail", args=["me",])


@pytest.mark.django_db
def test_updating_user(api_client, user):
    assert url == "/apis/user/me"
    api_client.force_authenticate(user)
    first_name = factory.Faker._get_faker().first_name()
    last_name = factory.Faker._get_faker().last_name()
    response = api_client.patch(
        url, data={"first_name": first_name, "last_name": last_name},
    )
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == first_name
    assert user.last_name == last_name


@pytest.mark.django_db
def test_updating_user__validations(api_client, user):
    api_client.force_authenticate(user)
    email = factory.Faker._get_faker().email()
    response = api_client.patch(url, data={"email": email},)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert not user.email == email
