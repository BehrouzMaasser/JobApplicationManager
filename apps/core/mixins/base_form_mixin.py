from django import forms


class BaseFormMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class)

        self._set_widget_attrs(form)

        return form

    def _set_widget_attrs(self, form):

        for name, field in form.fields.items():

            if isinstance(field, forms.DateTimeField):
                field.widget.input_type = "datetime-local"

            elif isinstance(field, forms.DateField):
                field.widget.input_type = "date-local"
