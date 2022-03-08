import typing

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from note_core.apis.note.serializers import NoteSerializer
from note_core.core.note.models import Note
from note_core.utilities.drf.permissions import OwnerPermission


class NoteViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Note.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
        OwnerPermission,
    ]
    lookup_field = "id"
    search_fields = [
        "title",
    ]

    def get_queryset(self):
        return self.request.user.notes.all()

    def get_serializer_class(self):
        return NoteSerializer

    @swagger_auto_schema(
        operation_summary="List Notes",
        operation_description="""
            List user Notes.
        """,
        tags=["Note",],
    )
    def list(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().list(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Note",
        operation_description="""
            Create Note.
        """,
        tags=["Note",],
    )
    def create(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().create(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Note",
        operation_description="""
            Update Note attributes (title/content)
        """,
        tags=["Note",],
    )
    def update(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().update(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Note",
        operation_description="""
            Retrieve Note
        """,
        tags=["Note",],
    )
    def retrieve(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().retrieve(request=request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Note",
        operation_description="""
            Delete Note
        """,
        tags=["Note",],
    )
    def destroy(
        self, request: Request, *args: typing.Any, **kwargs: typing.Any
    ) -> Response:
        return super().destroy(request=request, *args, **kwargs)
