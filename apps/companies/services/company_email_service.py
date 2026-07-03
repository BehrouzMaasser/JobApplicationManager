"""
Service layer for CompanyEmail domain logic.

This module handles creation, update, and deletion of email records
associated with a company while enforcing workspace and company-level
ownership rules.
"""

from typing import Any
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyEmail

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import CompanyChildContext

# Selectors
from apps.companies.selectors.company_email_selector import CompanyEmailSelector

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError


# Company Email Service
class CompanyEmailService(CompanyService):
    """
    Service responsible for managing CompanyEmail domain operations.

    Ensures strict workspace and company ownership validation for all operations.
    """

    CREATE_REQUIRED_FIELDS = {"title", "email"}
    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: CompanyChildContext,
        validated_data: dict[str, Any],
    ) -> CompanyEmail:
        """
        Create a new CompanyEmail under a company.

        Calls:
            _resolve_company() to retrieve the company context.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

            DomainInvariantViolationError:
                If the company does not belong to the workspace.

        Returns:
            CompanyEmail:
                The created company email instance.
        """

        company = CompanyEmailService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id,
        )

        instance = CompanyEmail(
            company=company,
            title=validated_data.get("title"),
            email=validated_data.get("email"),
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
    ) -> CompanyEmail:
        """
        Update an existing CompanyEmail instance.

        Calls:
            _resolve_company_email() to retrieve the target instance.
            _update_non_m2m_fields() to apply updates.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the CompanyEmail does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the email does not belong to the specified company or workspace.

            ValidationError:
                If model validation fails.

        Returns:
            CompanyEmail:
                The updated company email instance.
        """

        instance = CompanyEmailService._resolve_company_email(
            user=user,
            context=context,
        )

        CompanyEmailService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyEmailService.UPDATABLE_FIELDS,
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
        Delete a CompanyEmail instance.

        Calls:
            - _resolve_company_email() to retrieve the target instance.
            - django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the CompanyEmail does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the email does not belong to the specified company or workspace.

        Returns:
            None
        """

        instance = CompanyEmailService._resolve_company_email(
            user=user,
            context=context,
        )

        instance.delete()

    @staticmethod
    def _resolve_company_email(
        *,
        user: User,
        context: CompanyChildContext,
    ) -> CompanyEmail:
        """
        Resolve a CompanyEmail and validate workspace/company ownership.

        Calls:
            CompanyEmailSelector.get()

        Raises:
            ResourceNotFoundError:
                If the CompanyEmail does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the email does not belong to the company or workspace.

        Returns:
            CompanyEmail:
                The resolved company email instance.
        """

        company_email = CompanyEmailSelector.get(
            user=user,
            company_email_id=context.id,
        )

        if company_email.company_id != context.company_id:
            raise DomainInvariantViolationError(
                f"CompanyEmail {context.id} does not belong to "
                f"Company {context.company_id}"
            )

        if company_email.company.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"CompanyEmail {context.id}'s company {context.company_id} does not"
                f" belong to Workspace {context.workspace_id}"
            )

        return company_email
