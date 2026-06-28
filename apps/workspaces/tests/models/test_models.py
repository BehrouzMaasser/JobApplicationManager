from uuid import UUID

import pytest

# Django
from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Models
from apps.workspaces.models import Workspace


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceValidation:

    def test_workspace_requires_owner(self):
        with pytest.raises(ValidationError):
            Workspace(name="Test", owner=None).full_clean()

    def test_workspace_requires_name(self, user):
        with pytest.raises(ValidationError):
            Workspace(name=None, owner=user).full_clean()

    def test_workspace_requires_non_empty_name(self, user):
        with pytest.raises(ValidationError):
            Workspace(name="", owner=user).full_clean()


class TestWorkspaceConstraint:

    def test_workspace_name_is_unique_per_user(self, user):
        Workspace.objects.create(name="Workspace 1", owner=user)

        with pytest.raises(IntegrityError):
            Workspace.objects.create(name="Workspace 1", owner=user)


#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceCreation:

    def test_valid_workspace_creation(self, user):
        workspace = Workspace.objects.create(name="Workspace 1", owner=user)

        assert workspace.owner == user
        assert workspace.name == "Workspace 1"
        assert isinstance(workspace.workspace_id, UUID)
        assert workspace.created_at is not None
        assert workspace.updated_at is not None

    def test_ordering(self, user):
        workspace1 = Workspace.objects.create(name="A", owner=user)
        workspace2 = Workspace.objects.create(name="C", owner=user)
        workspace3 = Workspace.objects.create(name="B", owner=user)
        workspace4 = Workspace.objects.create(name="Workspace 2", owner=user)
        workspace5 = Workspace.objects.create(name="Workspace 1", owner=user)

        correct_name_order = [
            workspace1, workspace3, workspace2, workspace5, workspace4
        ]

        workspaces = Workspace.objects.all()

        for ws_correct_order, ws_given in zip(correct_name_order, workspaces):
            assert ws_correct_order == ws_given

    def test_other_users_with_same_workspace_name_is_valid(self, user, other_user):

        workspace1 = Workspace.objects.create(name="Workspace 1", owner=user)
        workspace2 = Workspace.objects.create(name="Workspace 1", owner=other_user)

        assert isinstance(workspace1.workspace_id, UUID)
        assert isinstance(workspace2.workspace_id, UUID)

        assert workspace1.owner == user
        assert workspace2.owner == other_user

        assert workspace1.name == "Workspace 1"
        assert workspace1.name == workspace2.name


class TestWorkspaceRepresentation:

    def test_workspace_string_representation(self, user):
        workspace1 = Workspace.objects.create(name="Workspace 1", owner=user)

        assert str(workspace1) == f"Workspace 1 ({user.email})"

#   ----------------------------------- ****** -----------------------------------
