from uuid import UUID

# Models

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.accounts.models import User
from apps.workspaces.models import Workspace

# Services
from apps.workspaces.services.base_service import BaseService


# Workspace Service
class WorkspaceService(BaseService):

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict) -> Workspace:

        instance = Workspace(
            owner=user,
            name=validated_data.get("name")
        )

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"Workspace": ["Invalid Dat Given", str(e)]})

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            workspace_id: UUID,
            validated_data: dict
    ) -> Workspace:

        instance = WorkspaceService._resolve_workspace(
            user=user, workspace_id=workspace_id
            )

        WorkspaceService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=WorkspaceService.UPDATABLE_FIELDS
        )

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"Workspace": ["Invalid Dat Given", str(e)]})

        return instance

    @staticmethod
    def remove(*, user: User, workspace_id: UUID) -> None:

        instance = WorkspaceService._resolve_workspace(
            user=user, workspace_id=workspace_id
        )

        instance.delete()

    @staticmethod
    def _resolve_workspace(*, user: User, workspace_id: UUID) -> Workspace:

        try:
            return Workspace.objects.get(
                owner=user,
                workspace_id=workspace_id
            )
        except Workspace.DoesNotExist:
            raise ValidationError({"Workspace": "Workspace does not exist!"})
