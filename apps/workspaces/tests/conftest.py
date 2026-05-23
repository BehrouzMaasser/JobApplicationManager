import pytest

from django.contrib.auth import get_user_model

from apps.workspaces.models import Workspace


User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user1@gmail.com", password="pass")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(email="user2@gmail.com", password="pass")


@pytest.fixture
def workspace1_user1_valid_data():

    return {"name": "Workspace 1"}


@pytest.fixture
def workspace1_user1_updated_valid_data():

    return {"name": "Workspace 1 Updated"}


@pytest.fixture
def workspace_user1(db, user):
    return Workspace.objects.create(
        name="Test Workspace",
        owner=user
    )


@pytest.fixture
def other_workspace_user1(db, user):
    return Workspace.objects.create(
        name="Other Workspace",
        owner=user
    )


@pytest.fixture
def workspace_user2(db, other_user):
    return Workspace.objects.create(
        name="Test Workspace",
        owner=other_user
    )
