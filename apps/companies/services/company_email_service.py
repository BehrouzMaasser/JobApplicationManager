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

        instance.full_clean()
        instance.save()

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

        company_email = CompanyEmailSelector.get(
            user=user, company_email_id=context.id
        )

        if company_email.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"Company Email {context.id} does not belong to Company"
                f" {context.company_id}"

            )

        return company_email
