from apps.core.view_contexts.app_context import AppContext
from apps.core.view_contexts.extra_context import ExtraContext


class AppContextMixin:

    def build_app_context(self):

        return AppContext()

    def build_extra_context(self):

        return ExtraContext()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["app_context"] = self.build_app_context()
        context["extra_context"] = self.build_extra_context()

        return context
