import pytest

from django.contrib.auth import get_user_model

from apps.testing.models import (
    DummyItem,
    DummyTag,
)


User = get_user_model()


# ---------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------

@pytest.fixture
def user1(db):
    """Primary user used throughout the BaseService contract tests."""

    return User.objects.create_user(
        email="user1@example.com",
        password="password123",
    )


@pytest.fixture
def user2(db):
    """Secondary user used for ownership validation tests."""

    return User.objects.create_user(
        email="user2@example.com",
        password="password123",
    )


# ---------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------

@pytest.fixture
def tag1_user1(user1):
    """Single tag owned by the primary user."""

    return DummyTag.objects.create(
        owner=user1,
        name="Python",
    )


@pytest.fixture
def tag2_user1(user1):
    """Another tag owned by the primary user."""

    return DummyTag.objects.create(
        owner=user1,
        name="Django",
    )


@pytest.fixture
def tag1_user2(user2):
    """Tag owned by another user."""

    return DummyTag.objects.create(
        owner=user2,
        name="Foreign",
    )


# ---------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------

@pytest.fixture
def item1(user1):
    """Persisted TestItem without tags."""

    return DummyItem.objects.create(
        owner=user1,
        name="Original",
    )


@pytest.fixture
def tagged1_item1(item1, tag1_user1):
    """Persisted TestItem with one tag."""

    item1.tags.add(tag1_user1)
    return item1


# ---------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------

class DummyContext:
    """
    Minimal context object expected by BaseService.

    Only exposes the `id` attribute required by _resolve_instance().
    """

    def __init__(self, obj_id):
        self.id = obj_id


@pytest.fixture
def context(item1):
    """Context pointing to an existing TestItem."""

    return DummyContext(item1.id)
