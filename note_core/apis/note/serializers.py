from rest_framework import serializers

from note_core.core.note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
        ]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs):
        user = self.context["request"].user
        attrs["user"] = user
        return attrs
