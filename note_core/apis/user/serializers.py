from rest_framework import serializers

from note_core.core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "title",
            "role",
            "date_joined",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
        }
