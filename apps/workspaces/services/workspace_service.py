"""
Business services for managing workspaces.

Contains operations responsible for creating, updating, and deleting
workspace instances while enforcing business rules.
"""

from typing import Any
from uuid import UUID

from django.db import transaction

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace

# Selectors
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Workspace Service
class WorkspaceService(BaseService):
    """
    Implements business operations for the Workspace domain.

    All persistence and business-rule validation related to workspaces
    should be performed through this service.
    """

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict[str, Any]) -> Workspace:
        """
        Create a workspace for a user.

        Validates the supplied data before persisting the workspace.

        Calls: In order
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            Workspace:
                The workspace instance created.
        """

        instance = Workspace(
            owner=user,
            name=validated_data.get("name")
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            workspace_id: UUID,
            validated_data: dict[str, Any]
    ) -> Workspace:
        """
        Update a workspace for a user.

        Validates the supplied data before persisting the workspace.

        Calls: In order
            _resolve_workspace() to retrieve the workspace instance to update.
            _update_non_m2m_fields() to assign the new values to the workspace.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the Workspace does not exist.

            AccessDeniedError:
                If the Workspace does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Workspace to update.

            ValidationError:
                If model validation fails.

        Returns:
            Workspace:
                The workspace instance updated.
        """

        instance = WorkspaceService._resolve_workspace(
            user=user, workspace_id=workspace_id
            )

        WorkspaceService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=WorkspaceService.UPDATABLE_FIELDS
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def remove(*, user: User, workspace_id: UUID) -> None:
        """
        Remove a workspace for a user from the database if the workspace exists.

        Calls: In order
            _resolve_workspace() to retrieve the workspace instance to update.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the Workspace does not exist.

            AccessDeniedError:
                If the Workspace does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Workspace to delete.

        Returns:
            None
        """

        instance = WorkspaceService._resolve_workspace(
            user=user, workspace_id=workspace_id
        )

        instance.delete()

    @staticmethod
    def _resolve_workspace(*, user: User, workspace_id: UUID) -> Workspace:
        """
        Retrieve a workspace from the Workspaces database.

        Calls:
            WorkspaceSelector.get()

        Raises:
            ResourceNotFoundError:
                If the Workspace does not exist.

            AccessDeniedError:
                If the Workspace does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Workspace.

        Returns:
            Workspace:
                The workspace retrieved from the database.
        """

        return WorkspaceSelector.get(user=user, workspace_id=workspace_id)
