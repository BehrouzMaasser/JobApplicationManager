from rest_framework.exceptions import ValidationError


class ServiceValidationErrorMixin:

    @staticmethod
    def add_service_errors_to_form(*, form, exception: ValidationError):

        details = exception.detail

        if isinstance(details, dict):

            for field, errors in details.items():

                if not isinstance(errors, list):
                    errors = [errors]

                for error in errors:
                    form.add_error(field, str(error))

        else:

            form.add_error(None, str(details))
