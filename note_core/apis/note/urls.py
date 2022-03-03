from django.urls import include, path

from note_core.apis.note.views import NoteViewSet
from note_core.utilities.drf.routers import CustomRouter

app_name = "Note"

router = CustomRouter(trailing_slash=False)
router.register(r"", NoteViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
