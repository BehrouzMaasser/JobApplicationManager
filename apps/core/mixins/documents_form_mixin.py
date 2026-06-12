from apps.core.mixins.base_form_mixin import BaseFormMixin
from apps.documents.selectors.document_type_selector import DocumentTypeSelector


class DocumentFormMixin(BaseFormMixin):

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        form.fields["document_type"].queryset = DocumentTypeSelector.list(
            user=self.request.user
        )

        return form
