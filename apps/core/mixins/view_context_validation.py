
class CreateViewContextValidationMixin:
    def dispatch(self, request, *args, **kwargs):
        self.validate_request_context()

        return super().dispatch(request, *args, **kwargs)

    def validate_request_context(self):
        raise NotImplementedError
