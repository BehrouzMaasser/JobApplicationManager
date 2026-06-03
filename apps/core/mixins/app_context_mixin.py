from apps.core.contexts.app_context import AppContext


class AppContextMixin:

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["app_context"] = self.build_app_context()

        return context
