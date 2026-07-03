"""
Service layer for Company domain logic.

This module contains all business operations related to Company entities,
including creation, update, and deletion, while enforcing workspace-level
invariants and validation rules.
"""

from typing import Any
from uuid import UUID

# Django
from django.db import transaction

# Contexts
from apps.companies.services.contexts.company_context import CompanyContext

# Models
from apps.companies.models import Company
from apps.accounts.models import User

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError

# Parent Service
from apps.workspaces.services.workspace_service import WorkspaceService

# Selectors
from apps.companies.selectors.company_selector import CompanySelector


# Company Service
class CompanyService(WorkspaceService):
    """
    Service responsible for handling Company domain operations.

    This service enforces workspace boundaries and delegates retrieval
    logic to selectors while ensuring validation consistency.
    """

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        "website",
    }

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: CompanyContext,
        validated_data: dict[str, Any],
    ) -> Company:
        """
        Create a new Company instance within a workspace.

        Calls: In order
            _resolve_workspace() to retrieve the workspace building the company in.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            Company:
                The company instance created.
        """

        workspace = CompanyService._resolve_workspace(
            user=user,
            workspace_id=context.workspace_id,
        )

        instance = Company(
            workspace=workspace,
            name=validated_data.get("name"),
            website=validated_data.get("website"),
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: CompanyContext,
        validated_data: dict[str, Any],
    ) -> Company:
        """
        Update an existing Company instance.

        Calls: In order
            _resolve_company() to retrieve the company instance to update.
            _update_non_m2m_fields() to assign the new values to the company.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the Company does not exist.

            AccessDeniedError:
                If the Company does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company to update.

            ValidationError:
                If model validation fails.

        Returns:
            Company:
                The Company instance updated.
        """

        instance = CompanyService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.id,
        )

        CompanyService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyService.UPDATABLE_FIELDS,
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    def remove(*, user: User, context: CompanyContext) -> None:
        """
        Remove a Company for a user from the database if the company exists.

        Calls: In order
            _resolve_company() to retrieve the company instance to update.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the Company does not exist.

            AccessDeniedError:
                If the Company does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company to delete.

        Returns:
            None
        """

        instance = CompanyService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.id,
        )

        instance.delete()

    @staticmethod
    def _resolve_company(
        *,
        user: User,
        workspace_id: UUID,
        company_id: int,
    ) -> Company:
        """
        Resolve and validate company ownership within a workspace.

        Calls:
            CompanySelector.get()

        Raises:
            ResourceNotFoundError:
                If the Company does not exist.

            AccessDeniedError:
                If the Company does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company.

            DomainInvariantViolationError:
                If the company does not belong to the workspace provided.

        Returns:
            Company:
                The company retrieved from the database.
        """

        company = CompanySelector.get(user=user, company_id=company_id)

        if company.workspace.workspace_id != workspace_id:
            raise DomainInvariantViolationError(
                f"Company {company_id} does not belong to Workspace {workspace_id}"
            )

        return company
