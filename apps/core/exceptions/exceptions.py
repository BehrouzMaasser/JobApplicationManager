# core/exceptions.py

class AppError(Exception):
    pass


class ResourceNotFoundError(AppError):

    def __init__(self, resource: str, message: str | None = None):

        self.resource = resource
        self._message_given = message

        super().__init__(self._message_given)

    @property
    def message(self):

        if self._message_given is None:
            return f"Resource {self.resource} not found"
        return self._message_given


class AccessDeniedError(AppError):

    def __init__(self, resource: str, message: str | None = None):

        self.resource = resource
        self._message_given = message

        super().__init__(self._message_given)

    @property
    def message(self):

        if self._message_given is None:
            return f"Access to {self.resource} was denied"
        return self._message_given


class BusinessRuleViolationError(AppError):

    def __init__(
            self,
            message: str | None = None,
            messages: None | list[str] = None,
            fields: None | list[str] = None
    ):

        self._message_given = message
        self.messages = messages
        self.fields = fields

        if self.messages is not None and len(self.messages) != len(self.fields):
            raise InfraStructureViolationError(
                "BusinessRuleViolationError raised error: Number of messages and "
                "fields do not match"
            )

        super().__init__(self._message_given)

    @property
    def message(self):

        if self._message_given is None:
            return f"Business rule violated"

        return f"Business rule violated: {self._message_given}"

    @property
    def details(self):

        if self.messages is not None:
            return {
                field: [self.messages[index]] for
                index, field in enumerate(self.fields)
            }

        return None


class InfraStructureViolationError(AppError):
    pass
