from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyEmail

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import CompanyChildContext


class CompanyEmailService(CompanyService):

    CREATE_REQUIRED_FIELDS = {"title", "email"}

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
            *,
            user: User,
            context: CompanyChildContext,
            validated_data: dict
    ) -> CompanyEmail:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company
        company = CompanyEmailService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id
        )

        instance = CompanyEmail(
            company=company,
            title=validated_data.get("title"),
            email=validated_data.get("email"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"email": ["Invalid Data Given", str(e)]})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            context: CompanyChildContext,
            validated_data: dict
    ) -> CompanyEmail:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company Note
        instance = CompanyEmailService._resolve_company_email(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        # Applying changes:
        CompanyEmailService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyEmailService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except (ValidationError, IntegrityError):
            raise ValidationError({"email": "Invalid Data Given"})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, context: CompanyChildContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company Note
        instance = CompanyEmailService._resolve_company_email(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_company_email(
            *,
            user: User,
            context: CompanyChildContext,
    ):
        company = CompanyEmailService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id
        )

        try:
            return company.company_emails.get(pk=context.id)
        except CompanyEmail.DoesNotExist:
            raise ValidationError({"email": "Email not found"})
