from apps.applications.selectors.application_selector import JobApplicationSelector
from apps.companies.services.job_position_service import JobPositionService
from apps.core.common.contexts.contexts import CompanyChildContext
from apps.core.mixins.view_context_validation import CreateViewContextValidationMixin


class JobPositionChildCreateViewContextValidationMixin(
    CreateViewContextValidationMixin
):

    def validate_request_context(self):

        JobPositionService._resolve_instance(
            user=self.request.user,
            context=CompanyChildContext(
                id=self.kwargs["job_position_id"],
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"],
            )
        )


class JobApplicationChildCreateViewContextValidationMixin(
    CreateViewContextValidationMixin
):

    def validate_request_context(self):

        JobApplicationSelector.get(
            user=self.request.user,
            obj_id=self.kwargs["job_application_id"],
        )
