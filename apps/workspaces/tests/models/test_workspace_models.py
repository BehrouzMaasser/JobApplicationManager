from uuid import UUID

import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

# Django
from django.db import models

# Models
from apps.workspaces.models import Workspace


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Define the Persistence Schema
# ---------------------------------------------------------------------------


class TestWorkspaceSchema:

    def test_workspace_creates_valid_instance(self, user1):
        workspace = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        assert workspace.owner == user1
        assert workspace.name == "Workspace 1"

    def test_workspace_generates_uuid_identifier(self, user1):
        workspace = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        assert isinstance(workspace.workspace_id, UUID)

    def test_workspace_sets_creation_timestamp(self, user1):
        workspace = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        assert workspace.created_at is not None

    def test_workspace_sets_update_timestamp(self, user1):
        workspace = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        assert workspace.updated_at is not None

    def test_workspace_ordering_is_by_name(self, user1):
        workspace_c = Workspace.objects.create(
            name="C",
            owner=user1,
        )
        workspace_a = Workspace.objects.create(
            name="A",
            owner=user1,
        )
        workspace_b = Workspace.objects.create(
            name="B",
            owner=user1,
        )

        workspaces = list(Workspace.objects.all())

        assert workspaces == [
            workspace_a,
            workspace_b,
            workspace_c,
        ]

    def test_workspace_has_owner_relationship(self):
        field = Workspace._meta.get_field("owner")

        assert isinstance(field, models.ForeignKey)

    def test_workspace_has_workspace_id_field(self):
        field = Workspace._meta.get_field("workspace_id")

        assert isinstance(field, models.UUIDField)
        assert field.editable is False
        assert field.unique is True


class TestWorkspaceConstraints:

    def test_workspace_name_is_unique_per_owner(self, user1):
        Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        with pytest.raises(IntegrityError):
            Workspace.objects.create(
                name="Workspace 1",
                owner=user1,
            )

    def test_workspace_constraint_validation_returns_correct_error_code(
        self,
        user1,
    ):
        Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        with pytest.raises(ValidationError) as exc:

            Workspace(
                name="Workspace 1",
                owner=user1
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_workspace_name"
        )

    def test_same_workspace_name_is_allowed_for_different_users(
        self,
        user1,
        user2,
    ):
        workspace1 = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        workspace2 = Workspace.objects.create(
            name="Workspace 1",
            owner=user2,
        )

        assert workspace1.name == workspace2.name
        assert workspace1.owner != workspace2.owner


# ---------------------------------------------------------------------------
# M-02: Enforce Domain Invariants
# ---------------------------------------------------------------------------


class TestWorkspaceValidation:

    def test_workspace_requires_owner(self):
        workspace = Workspace(
            name="Workspace 1",
            owner=None,
        )

        with pytest.raises(ValidationError):
            workspace.full_clean()

    def test_workspace_requires_name(self, user1):
        workspace = Workspace(
            name=None,
            owner=user1,
        )

        with pytest.raises(ValidationError):
            workspace.full_clean()

    def test_workspace_name_cannot_be_blank(self, user1):
        workspace = Workspace(
            name="",
            owner=user1,
        )

        with pytest.raises(ValidationError):
            workspace.full_clean()


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestWorkspaceProperties:

    def test_workspace_string_representation(self, user1):
        workspace = Workspace.objects.create(
            name="Workspace 1",
            owner=user1,
        )

        assert str(workspace) == f"Workspace 1 ({user1.email})"
