from django.core.exceptions import ValidationError

from apps.core.exceptions.exceptions import BusinessRuleViolationError


class ServiceFormErrorMixin:

    def execute_service(self, *, form, operation):

        try:
            operation()

        except (ValidationError, BusinessRuleViolationError) as err:

            self.add_service_errors_to_form(
                form=form,
                exception=err,
            )

            return self.form_invalid(form=form)

        return None

    @staticmethod
    def add_service_errors_to_form(*, form, exception):

        if isinstance(exception, BusinessRuleViolationError):

            for field, message in zip(exception.fields, exception.messages):
                form.add_error(field, message)

        if isinstance(exception, ValidationError):

            if hasattr(exception, "message_dict"):
                for field, errors in exception.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)

            else:
                for error in exception.messages:
                    form.add_error(None, error)

            return
