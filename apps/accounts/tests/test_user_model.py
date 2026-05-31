import pytest
import uuid

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.core.exceptions import ValidationError


User = get_user_model()


@pytest.mark.django_db
class TestUserModel:

    def test_user_str_returns_email(self):

        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        assert str(user) == "test@example.com"

    def test_documents_directory_auto_generated(self):

        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        assert user.documents_directory is not None
        assert isinstance(user.documents_directory, uuid.UUID)

    @override_settings(
        PASSWORD_HASHERS=[
            "django.contrib.auth.hashers.MD5PasswordHasher"
        ]
    )
    def test_documents_directory_is_unique(self):

        users = []

        for _ in range(2):
           users.append(
               User.objects.create_user(
                   email=f"test{_}@example.com",
                   password="testpass123"
               )
           )

        user_directories = [str(user.documents_directory) for user in users]

        assert len(user_directories) == len(set(user_directories))

    def test_created_at_is_set(self):

        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        assert user.created_at is not None

    def test_updated_at_changes_on_save(self):

        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        original_updated_at = user.updated_at

        user.first_name = "Updated"

        user.save()
        user.refresh_from_db()

        assert user.updated_at >= original_updated_at

    def test_email_must_be_unique(self):

        User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )

        with pytest.raises(ValidationError):
            User(email="test@example.com").full_clean()

    def test_invalid_email_validation(self):

        user = User(email="invalid-email")

        with pytest.raises(ValidationError):
            user.full_clean()
