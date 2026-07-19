from uuid import UUID

import pytest

from django.core.exceptions import ValidationError

from apps.core.common.contexts.contexts import (
    EmptyContext,
    WorkspaceContext,
)
from apps.core.exceptions.exceptions import (
    InfrastructureViolationError,
)
from apps.workspaces.models import Workspace
from apps.workspaces.services.workspace_service import WorkspaceService


pytestmark = pytest.mark.django_db


@pytest.fixture
def workspace1_user1_valid_data():

    return {"name": "Workspace 1"}


@pytest.fixture
def workspace1_user1_updated_valid_data():

    return {"name": "Workspace 1 Updated"}


EMPTY_CONTEXT = EmptyContext()


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

class TestWorkspaceServiceHooks:

    def test_resolve_create_dependencies_assigns_current_user_as_owner(
        self,
        user1,
    ):
        dependencies = WorkspaceService._resolve_create_dependencies(
            user=user1,
            context=EMPTY_CONTEXT,
        )

        assert dependencies == {
            "owner": user1,
        }


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

class TestWorkspaceServiceCreate:

    def test_create_assigns_owner_from_user(
        self,
        user1,
        workspace1_user1_valid_data,
    ):

        workspace = WorkspaceService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=workspace1_user1_valid_data,
        )

        assert isinstance(
            workspace.workspace_id,
            UUID,
        )

        assert workspace.owner == user1
        assert workspace.name == (
            workspace1_user1_valid_data["name"]
        )

    def test_create_ignores_owner_from_payload(
        self,
        user1,
        user2,
    ):

        workspace = WorkspaceService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data={
                "name": "Workspace",
                "owner": user2,
            },
        )

        assert workspace.owner == user1

    def test_create_duplicate_name_raises_validation_error(
        self,
        user1,
        workspace1_user1_valid_data,
    ):

        WorkspaceService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=workspace1_user1_valid_data,
        )

        with pytest.raises(ValidationError):
            WorkspaceService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data=workspace1_user1_valid_data,
            )


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

class TestWorkspaceServiceUpdate:

    def test_update_changes_name(
        self,
        user1,
        workspace1_user1,
        workspace1_user1_updated_valid_data,
    ):

        workspace = WorkspaceService.update(
            user=user1,
            context=WorkspaceContext(
                id=workspace1_user1.workspace_id
            ),
            validated_data=workspace1_user1_updated_valid_data,
        )

        assert workspace.name == (
            workspace1_user1_updated_valid_data["name"]
        )

        assert workspace.owner == user1

    def test_update_does_not_change_owner(
        self,
        user1,
        user2,
        workspace1_user1,
    ):

        workspace = WorkspaceService.update(
            user=user1,
            context=WorkspaceContext(
                id=workspace1_user1.workspace_id
            ),
            validated_data={
                "owner": user2,
            },
        )

        assert workspace.owner == user1

    def test_update_duplicate_name_raises_validation_error(
        self,
        user1,
        workspace1_user1,
        workspace2_user1,
    ):

        with pytest.raises(ValidationError):
            WorkspaceService.update(
                user=user1,
                context=WorkspaceContext(
                    id=workspace2_user1.workspace_id
                ),
                validated_data={
                    "name": workspace1_user1.name,
                },
            )


# ---------------------------------------------------------------------------
# Remove
# ---------------------------------------------------------------------------

class TestWorkspaceServiceRemove:

    def test_remove_deletes_workspace(
        self,
        user1,
        workspace1_user1,
    ):

        workspace_id = workspace1_user1.workspace_id

        WorkspaceService.remove(
            user=user1,
            context=WorkspaceContext(
                id=workspace_id
            ),
        )

        assert not Workspace.objects.filter(
            workspace_id=workspace_id
        ).exists()


# ---------------------------------------------------------------------------
# Infrastructure handling
# ---------------------------------------------------------------------------

class TestWorkspaceServiceInfrastructure:

    def test_unexpected_exception_is_translated(
        self,
        user1,
        monkeypatch,
    ):

        def raise_error(*args, **kwargs):
            raise RuntimeError("database exploded")

        monkeypatch.setattr(
            WorkspaceService,
            "_save",
            raise_error,
        )

        with pytest.raises(
            InfrastructureViolationError
        ):
            WorkspaceService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data={
                    "name": "Workspace",
                },
            )
