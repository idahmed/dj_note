import typing

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from note_core.apis.user.permissions import UserPermission
from note_core.apis.user.serializers import UserSerializer
from note_core.core.user.models import User


class UserViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch"]
    queryset = User.objects.all()
    permission_classes = [
        UserPermission,
    ]
    lookup_field = "username"
    search_fields = ["email", "first_name", "last_name"]

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        return UserSerializer

    @swagger_auto_schema(
        operation_summary="Create user",
        operation_description="""
            Create user (the tenant owner and first user)
        """,
        tags=["user",],
    )
    def create(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().create(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user",
        operation_description="""
            Update user attributes (first/last name)
        """,
        tags=["user",],
    )
    def update(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().update(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve user",
        operation_description="""
            Retrieve user
        """,
        tags=["user",],
    )
    def retrieve(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().retrieve(request=request, *args, **kwargs)
