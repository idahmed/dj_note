from django.contrib import admin

from note_core.core.note.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    search_fields = [
        "title",

    ]
    list_display = [
        "title",
        "created_at",
        "updated_at",
    ]

    class Meta:
        model = Note
