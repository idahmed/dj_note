from django.contrib import admin

from note_core.core.user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = [
        "email",
        "first_name",
        "last_name",
    ]
    list_display = [
        "id",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    ]

    class Meta:
        model = User
