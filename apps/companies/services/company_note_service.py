"""
Service layer for CompanyNote domain logic.

This module handles creation, update, and deletion of notes associated
with a company, ensuring workspace and company-level ownership validation.
"""

from typing import Any
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyNote

# Selectors
from apps.companies.selectors.company_note_selector import CompanyNoteSelector

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyChildContext
)

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError


# Company Note Service
class CompanyNoteService(CompanyService):
    """
    Service responsible for managing CompanyNote domain operations.

    Ensures that notes are always accessed within the correct company
    and workspace boundaries.
    """

    CREATE_REQUIRED_FIELDS = {
        "title",
        "content",
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: CompanyChildContext,
        validated_data: dict[str, Any],
    ) -> CompanyNote:
        """
        Create a new CompanyNote under a company.

        Calls: In order
            _resolve_company() to retrieve the company building the company note in.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            CompanyNote:
                The company instance created.
        """

        company = CompanyNoteService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id,
        )

        instance = CompanyNote(
            company=company,
            title=validated_data.get("title"),
            content=validated_data.get("content"),
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: CompanyChildContext,
        validated_data: dict[str, Any],
    ) -> CompanyNote:
        """
        Update an existing CompanyNote instance.

        Calls: In order
            _resolve_company_note() to retrieve the company note instance to update.
            _update_non_m2m_fields() to assign the new values to the company note.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the Company Note does not exist.

            AccessDeniedError:
                If the Company Note does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company Note to update.

            ValidationError:
                If model validation fails.

        Returns:
            Company:
                The Company Note instance updated.
        """

        instance = CompanyNoteService._resolve_company_note(
            user=user,
            context=context,
        )

        CompanyNoteService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyNoteService.UPDATABLE_FIELDS,
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def remove(
        *,
        user: User,
        context: CompanyChildContext,
    ) -> None:
        """
        Delete a CompanyNote for a user from the database if the company note exists.

        Calls: In order
            _resolve_company_note() to retrieve the company note instance to update.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the Company Note does not exist.

            AccessDeniedError:
                If the Company Note does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company Note to delete.

        Returns:
            None
        """

        instance = CompanyNoteService._resolve_company_note(
            user=user,
            context=context,
        )

        instance.delete()

    @staticmethod
    def _resolve_company_note(
        *,
        user: User,
        context: CompanyChildContext,
    ) -> CompanyNote:
        """
        Resolve a company note and validate workspace/company ownership.

        Calls:
            CompanyNoteSelector.get()

        Raises:
            ResourceNotFoundError:
                If the Company Note does not exist.

            AccessDeniedError:
                If the Company Note does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company Note.

            DomainInvariantViolationError:
                If the company of the company note does not belong to the workspace
                 provided.

                If the company note does not belong to the company provided.

        Returns:
            CompanyNote:
                The company note retrieved from the database.
        """

        company_note = CompanyNoteSelector.get(
            user=user,
            company_note_id=context.id,
        )

        if company_note.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"Company Note {context.id} does not belong to Company "
                f"{context.company_id}"
            )

        if company_note.company.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"Company Note {context.id}'s company {context.company_id} does not"
                f" belong to Workspace {context.workspace_id}"
            )

        return company_note
