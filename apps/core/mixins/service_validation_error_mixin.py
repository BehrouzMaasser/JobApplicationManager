from django.core.exceptions import ValidationError

from apps.core.exceptions.exceptions import BusinessRuleViolationError


class ServiceValidationErrorMixin:

    @staticmethod
    def add_service_errors_to_form(*, form, exception):

        if isinstance(exception, ValidationError):

            if hasattr(exception, "message_dict"):
                for field, errors in exception.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)

            else:
                for error in exception.messages:
                    form.add_error(None, error)

            return

        if isinstance(exception, BusinessRuleViolationError):

            for field, message in zip(exception.fields, exception.messages):
                form.add_error(field, message)
