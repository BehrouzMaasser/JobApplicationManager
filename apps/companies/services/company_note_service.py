from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyNote
from apps.companies.selectors.company_note_selector import CompanyNoteSelector

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyChildContext
)
from apps.core.exceptions.exceptions import BusinessRuleViolationError


# Company Note Service
class CompanyNoteService(CompanyService):

    CREATE_REQUIRED_FIELDS = {
        "title",
        "content"
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
            *,
            user: User,
            context: CompanyChildContext,
            validated_data: dict
    ) -> CompanyNote:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company
        company = CompanyNoteService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id
        )

        instance = CompanyNote(
            company=company,
            title=validated_data.get("title"),
            content=validated_data.get("content"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            context: CompanyChildContext,
            validated_data: dict
    ) -> CompanyNote:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company Note
        instance = CompanyNoteService._resolve_company_note(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        # Applying changes:
        CompanyNoteService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyNoteService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, context: CompanyChildContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company Note
        instance = CompanyNoteService._resolve_company_note(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_company_note(
            user: User, context: CompanyChildContext
    ) -> CompanyNote:

        company_note = CompanyNoteSelector.get(
            user=user, company_note_id=context.id
        )

        if company_note.company.pk != context.company_id:
            raise BusinessRuleViolationError(
                f"Company Note {company_note.pk} does not belong to "
                f"company {context.company_id}"
            )

        return company_note
