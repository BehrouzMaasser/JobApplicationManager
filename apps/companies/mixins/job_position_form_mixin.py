from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector
from apps.companies.selectors.job_task_selector import JobTaskSelector
from apps.core.mixins.base_form_mixin import BaseFormMixin


class JobPositionFormMixin(BaseFormMixin):

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
