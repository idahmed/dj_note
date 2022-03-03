import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_pending_migration(capsys):
    """Make sure there's no pending migration."""

    call_command("makemigrations", "--check", "--dry-run")

    captured = capsys.readouterr()
    assert captured.out == "No changes detected\n"
