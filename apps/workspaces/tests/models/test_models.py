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

    def test_workspace_requires_name(self, user1):
        with pytest.raises(ValidationError):
            Workspace(name=None, owner=user1).full_clean()

    def test_workspace_requires_non_empty_name(self, user1):
        with pytest.raises(ValidationError):
            Workspace(name="", owner=user1).full_clean()


class TestWorkspaceConstraint:

    def test_workspace_name_is_unique_per_user1(self, user1):
        Workspace.objects.create(name="Workspace 1", owner=user1)

        with pytest.raises(IntegrityError):
            Workspace.objects.create(name="Workspace 1", owner=user1)


#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceCreation:

    def test_valid_workspace_creation(self, user1):
        workspace = Workspace.objects.create(name="Workspace 1", owner=user1)

        assert workspace.owner == user1
        assert workspace.name == "Workspace 1"
        assert isinstance(workspace.workspace_id, UUID)
        assert workspace.created_at is not None
        assert workspace.updated_at is not None

    def test_ordering(self, user1):
        workspace1 = Workspace.objects.create(name="A", owner=user1)
        workspace2 = Workspace.objects.create(name="C", owner=user1)
        workspace3 = Workspace.objects.create(name="B", owner=user1)
        workspace4 = Workspace.objects.create(name="Workspace 2", owner=user1)
        workspace5 = Workspace.objects.create(name="Workspace 1", owner=user1)

        correct_name_order = [
            workspace1, workspace3, workspace2, workspace5, workspace4
        ]

        workspaces = Workspace.objects.all()

        for ws_correct_order, ws_given in zip(correct_name_order, workspaces):
            assert ws_correct_order == ws_given

    def test_other_user1s_with_same_workspace_name_is_valid(self, user1, user2):

        workspace1 = Workspace.objects.create(name="Workspace 1", owner=user1)
        workspace2 = Workspace.objects.create(name="Workspace 1", owner=user2)

        assert isinstance(workspace1.workspace_id, UUID)
        assert isinstance(workspace2.workspace_id, UUID)

        assert workspace1.owner == user1
        assert workspace2.owner == user2

        assert workspace1.name == "Workspace 1"
        assert workspace1.name == workspace2.name


class TestWorkspaceRepresentation:

    def test_workspace_string_representation(self, user1):
        workspace1 = Workspace.objects.create(name="Workspace 1", owner=user1)

        assert str(workspace1) == f"Workspace 1 ({user1.email})"

#   ----------------------------------- ****** -----------------------------------
