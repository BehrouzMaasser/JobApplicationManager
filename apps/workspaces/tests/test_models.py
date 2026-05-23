import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.workspaces.models import Workspace


#   ----------------------------------- ****** -----------------------------------

# Invalid Workspace Creation:

@pytest.mark.django_db
def test_workspace_requires_owner():

    workspace = Workspace(name="Test", owner=None)

    with pytest.raises(ValidationError):
        workspace.full_clean()


@pytest.mark.django_db
def test_workspace_requires_name(user):

    workspace = Workspace(name=None, owner=user)

    with pytest.raises(ValidationError):
        workspace.full_clean()


@pytest.mark.django_db
def test_workspace_requires_non_empty_name(user):

    workspace = Workspace(name="", owner=user)

    with pytest.raises(ValidationError):
        workspace.full_clean()


# Constraint Check:

@pytest.mark.django_db
def test_workspace_name_is_unique_per_user(user):

    Workspace.objects.create(name="Workspace 1", owner=user)

    with pytest.raises(IntegrityError):
        Workspace.objects.create(name="Workspace 1", owner=user)


#   ----------------------------------- ****** -----------------------------------


# Valid Workspace Creation:
@pytest.mark.django_db
def test_valid_workspace_creation(user):
    workspace = Workspace.objects.create(name="Workspace 1", owner=user)

    assert workspace.owner == user
    assert workspace.name == "Workspace 1"


@pytest.mark.django_db
def test_other_users_with_same_workspace_name(user, other_user):
    workspace1 = Workspace.objects.create(name="Workspace 1", owner=user)
    workspace2 = Workspace.objects.create(name="Workspace 1", owner=other_user)

    assert workspace1.owner == user
    assert workspace2.owner == other_user

    assert workspace1.name == "Workspace 1"
    assert workspace1.name == workspace2.name

#   ----------------------------------- ****** -----------------------------------
