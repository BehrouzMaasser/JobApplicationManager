from apps.companies.selectors.company_email_selector import CompanyEmailSelector
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector
from apps.companies.selectors.job_task_selector import JobTaskSelector
from apps.documents.selectors.document_selector import DocumentSelector


class JobPositionFormMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        form.fields["tasks"].queryset = JobTaskSelector.list(
            user=self.request.user
        )

        form.fields["benefits"].queryset = JobBenefitSelector.list(
            user=self.request.user
        )

        form.fields["requirements"].queryset = JobRequirementSelector.list(
            user=self.request.user
        )

        return form
