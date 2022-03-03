from datetime import timedelta
from functools import partial

import mock
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, aware_utcnow

from note_core.core.user.models import User


class TestAuth(APITestCase):
    login_url = reverse("auth:token_obtain")
    refresh_token_url = reverse("auth:token_refresh")
    logout_url = reverse("auth:token_revoke")
    testing_url = reverse("user:user-detail", args=["me",])

    email = "test@user.com"
    password = "somepassword"

    def setUp(self):
        self.user = User.objects.create_user(self.email, self.password)
        self.user_data = {"email": self.email, "password": self.password}

    def _login(self):
        r = self.client.post(self.login_url, self.user_data)
        body = r.json()
        if "access" in body:
            self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % body["access"])
        return r.status_code, body

    def test_logout_response_200(self):
        _, body = self._login()
        data = {"refresh": body["refresh"]}
        r = self.client.post(self.logout_url, data)
        body = r.content
        self.assertEquals(r.status_code, 204)
        self.assertFalse(body, body)

    def test_logout_with_bad_refresh_token_response_400(self):
        self._login()
        data = {"refresh": "dsf.sdfsdf.sdf"}
        r = self.client.post(self.logout_url, data)
        self.assertEquals(r.status_code, 400)

    def test_logout_refresh_token_in_blacklist(self):
        _, body = self._login()
        r = self.client.post(self.logout_url, body)
        self.assertEquals(r.status_code, 204)
        token = partial(RefreshToken, body["refresh"])
        self.assertRaises(TokenError, token)

    def test_access_token_invalid_in_hour_after_logout(self):
        _, body = self._login()
        self.client.post(self.logout_url, body)
        m = mock.Mock()
        m.return_value = aware_utcnow() + timedelta(minutes=60)
        with mock.patch("rest_framework_simplejwt.tokens.aware_utcnow", m):
            r = self.client.get(self.testing_url)
        self.assertEquals(r.status_code, 401)
