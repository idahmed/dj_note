from django.urls import include, path

from note_core.apis.user.views import UserViewSet
from note_core.utilities.drf.routers import CustomRouter

app_name = "user"

router = CustomRouter(trailing_slash=False)
router.register(r"", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
