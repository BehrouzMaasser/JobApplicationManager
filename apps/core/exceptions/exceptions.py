# core/exceptions.py

class AppError(Exception):
    pass


class DomainInvariantViolationError(AppError):
    """The application's domain state is inconsistent."""

    def __init__(self, message: str):

        self.message = message

        super().__init__(self.message)


class ResourceNotFoundError(AppError):

    def __init__(self, resource: str, message: str | None = None):

        self.resource = resource
        self._message = message

        super().__init__(self._message)

    @property
    def message(self):

        if self._message is None:
            return f"Resource {self.resource} not found"
        return self._message


class AccessDeniedError(AppError):

    def __init__(self, resource: str, message: str | None = None):

        self.resource = resource
        self._message = message

        super().__init__(self._message)

    @property
    def message(self):

        if self._message is None:
            return f"Access to {self.resource} was denied"
        return self._message


class BusinessRuleViolationError(AppError):

    def __init__(
            self,
            messages: None | list[str] = None,
            fields: None | list[str] = None
    ):

        self.messages = messages
        self.fields = fields

        if self.messages is not None and len(self.messages) != len(self.fields):
            raise InfraStructureViolationError(
                "BusinessRuleViolationError raised error: Number of messages and "
                "fields do not match"
            )

    @property
    def message(self):

        return f"Business rule violated"

    @property
    def details(self):

        if self.messages is not None:
            return {
                field: message for field, message in zip(self.fields, self.messages)
            }

        return None


class InfraStructureViolationError(AppError):
    pass
