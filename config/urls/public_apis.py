from os.path import join

from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class SchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(SchemaGenerator, self).get_schema(request, public)
        schema.basePath = join(schema.basePath, "apis/")
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        basePath="/apis/",
        # TODO: change terms link
        terms_of_service="https://www.newsbytes.com/",
        license=openapi.License(name="Privately owned"),
    ),
    public=True,
    urlconf="config.urls.public_apis",
    permission_classes=(permissions.AllowAny,),
    generator_class=SchemaGenerator,
)

urlpatterns = [
    # Docs
    url(
        "docs", schema_view.with_ui("redoc", cache_timeout=0), name="schema-swagger-ui",
    ),
    # Auth
    path("auth", include("note_core.apis.auth.urls", namespace="auth")),
    # User
    path("user", include("note_core.apis.user.urls", namespace="user")),
]
