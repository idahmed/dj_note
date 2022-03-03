from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path

urlpatterns = [
    # TODO: Develop a health check service (test db reachability, MQ and redis, etc)
    url(
        r"^$",
        lambda request: HttpResponse(
            "Yes I am alive!!!", content_type="application/json"
        ),
        name="ping",
    ),
    # Admin URLs
    path(f"admin/", admin.site.urls),
    # Public API Views
    path(f"apis/", include("config.urls.public_apis")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
