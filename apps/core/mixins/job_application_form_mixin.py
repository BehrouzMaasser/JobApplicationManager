from apps.companies.selectors.company_email_selector import CompanyEmailSelector
from apps.documents.selectors.document_selector import DocumentSelector


class JobApplicationFormMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        application = getattr(self, "object", None)

        if application:
            form.fields["emails"].queryset = CompanyEmailSelector.list(
                user=self.request.user,
                filters=CompanyEmailSelector.QueryFilter(
                    company_id=application.job_position.company.pk,
                )
            )
        else:
            form.fields["emails"].queryset = CompanyEmailSelector.list(
                user=self.request.user,
                filters=CompanyEmailSelector.QueryFilter(
                    company_id=self.kwargs["company_id"],
                )
            )

        form.fields["documents"].queryset = DocumentSelector.list(
            user=self.request.user
        )

        return form
