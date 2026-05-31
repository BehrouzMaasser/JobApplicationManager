import pytest

from django.contrib.auth import get_user_model


User = get_user_model()


@pytest.mark.django_db
class TestUserManager:

    def test_create_user_success(self):

        user = User.objects.create_user(
            email="TEST@Example.COM",
            password="testpass123"
        )

        assert user.email == "TEST@example.com".lower()
        assert user.check_password("testpass123")
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.is_active is True
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.phone_number is None
        assert user.date_of_birth is None

    def test_create_user_without_email_raises_error(self):

        with pytest.raises(ValueError, match="Users must have an email address"):
            User.objects.create_user(
                email="",
                password="testpass123"
            )

    def test_create_user_without_password_raises_error(self):

        with pytest.raises(ValueError, match="Users must have password"):
            User.objects.create_user(
                email="test@example.com",
                password=""
            )

    def test_create_user_with_is_staff_true_raises_error(self):

        with pytest.raises(ValueError, match="User must NOT have is_staff=True"):
            User.objects.create_user(
                email="test@example.com",
                password="testpass123",
                is_staff=True
            )

    def test_create_user_with_is_superuser_true_raises_error(self):

        with pytest.raises(ValueError, match="User must NOT have is_superuser=True"):
            User.objects.create_user(
                email="test@example.com",
                password="testpass123",
                is_superuser=True
            )

    def test_create_superuser_success(self):

        user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )

        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_active is True
        assert user.check_password("adminpass123")
        assert user.first_name == ""
        assert user.last_name == ""
        assert user.phone_number is None
        assert user.date_of_birth is None

    def test_create_superuser_with_is_staff_false_raises_error(self):

        with pytest.raises(ValueError, match="Superuser must have is_staff=True"):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpass123",
                is_staff=False
            )

    def test_create_superuser_with_is_superuser_false_raises_error(self):

        with pytest.raises(
                ValueError, match="Superuser must have is_superuser=True"
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpass123",
                is_superuser=False
            )
