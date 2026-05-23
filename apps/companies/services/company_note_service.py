from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyNote

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyChildContext
)


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

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"company_note": ["Invalid Data Given", str(e)]})

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

        try:
            instance.full_clean()
            instance.save()
        except (ValidationError, IntegrityError):
            raise ValidationError({"company_note": "Invalid Data Given"})

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

        company = CompanyNoteService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id
        )

        try:
            return company.company_notes.get(pk=context.id)
        except CompanyNote.DoesNotExist:
            raise ValidationError({"company_note": "Company Note does not exist"})
