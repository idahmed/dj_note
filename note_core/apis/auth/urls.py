from django.conf.urls import url
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from note_core.apis.auth.views import LogoutView

app_name = "auth"

urlpatterns = [
    url("^/token$", TokenObtainPairView.as_view(), name="token_obtain"),
    url("^/token/refresh$", TokenRefreshView.as_view(), name="token_refresh"),
    url("^/token/revoke$", LogoutView.as_view(), name="token_revoke"),
]
