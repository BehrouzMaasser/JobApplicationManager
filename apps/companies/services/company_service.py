from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError

# Contexts
from apps.companies.services.contexts.company_context import CompanyContext

# Models
from apps.companies.models import Company
from apps.accounts.models import User

# Parent Service
from apps.workspaces.services.workspace_service import WorkspaceService


# Services
class CompanyService(WorkspaceService):

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        "website"
    }

    @staticmethod
    @transaction.atomic
    def create(
            *,
            user: User,
            context: CompanyContext,
            validated_data: dict
    ) -> Company:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Workspace
        workspace = CompanyService._resolve_workspace(
            user=user,
            workspace_id=context.workspace_id
        )

        instance = Company(
            workspace=workspace,
            name=validated_data.get("name"),
            website=validated_data.get("website"),
        )

        # ----------------------*****---------------------

        # Model verification and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"Company": ["Invalid Company Data", str(e)]})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            context: CompanyContext,
            validated_data: dict
    ) -> Company:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Company
        instance = CompanyService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.id
        )

        # ----------------------*****---------------------

        # Applying changes:
        CompanyService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=CompanyService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except (ValidationError, IntegrityError):
            raise ValidationError({"Company": "Invalid Company Data"})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, context: CompanyContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Workspace
        instance = CompanyService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_company(
            *, user: User, workspace_id: UUID, company_id: str
    ) -> Company:

        workspace = CompanyService._resolve_workspace(
            user=user,
            workspace_id=workspace_id
        )

        try:
            return workspace.companies.get(pk=company_id)
        except Company.DoesNotExist:
            raise ValidationError({"Company": "Company does not exist"})
