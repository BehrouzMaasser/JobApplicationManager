import pytest

from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


@pytest.mark.django_db
def test_user_can_authenticate_with_email():

    User.objects.create_user(
        email="test@example.com",
        password="testpass123"
    )

    user = authenticate(
        email="test@example.com",
        password="testpass123"
    )

    assert user is not None
