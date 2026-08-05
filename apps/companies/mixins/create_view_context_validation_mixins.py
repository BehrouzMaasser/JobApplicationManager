from apps.companies.services.company_service import CompanyService
from apps.core.common.contexts.contexts import (
    WorkspaceContext,
    CompanyContext
)
from apps.core.mixins.view_context_validation import CreateViewContextValidationMixin
from apps.workspaces.services.workspace_service import WorkspaceService


class WorkspaceChildCreateViewContextValidationMixin(
    CreateViewContextValidationMixin
):

    def validate_request_context(self):

        WorkspaceService._resolve_instance(
            user=self.request.user,
            context=WorkspaceContext(
                id=self.kwargs["workspace_id"],
            )
        )


class CompanyChildCreateViewContextValidationMixin(
    CreateViewContextValidationMixin
):

    def validate_request_context(self):

        CompanyService._resolve_instance(
            user=self.request.user,
            context=CompanyContext(
                id=self.kwargs["company_id"],
                workspace_id=self.kwargs["workspace_id"],
            )
        )
