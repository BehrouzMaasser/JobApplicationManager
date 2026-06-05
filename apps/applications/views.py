from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Models
from apps.applications.models import JobApplication

# Selectors
from apps.applications.selectors.application_selector import JobApplicationSelector

# Services
from apps.applications.services.application_service import JobApplicationService

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationContext
)

# View Contexts and Mixins
from apps.core.contexts.app_context import AppContext
from apps.core.mixins.app_context_mixin import AppContextMixin
from apps.core.mixins.job_application_form_mixin import JobApplicationFormMixin


def application_list_url(workspace_id=None, company_id=None, job_position_id=None):

    params = {
            "workspace_id": workspace_id,
            "company_id": company_id,
            "job_position_id": job_position_id,
    }

    params = {param: value for param, value in params.items() if value is not None}

    return f"{reverse('job-application-list-web')}?{urlencode(params)}"


class JobApplicationListView(LoginRequiredMixin, AppContextMixin, ListView):

    model = JobApplication
    template_name = "applications/job_application/list.html"
    context_object_name = "job_applications"

    def get_queryset(self):

        return JobApplicationSelector.list(
            user=self.request.user,
            filters=JobApplicationSelector.QueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
                company_id=self.request.GET.get("company_id"),
                job_position_id=self.request.GET.get("job_position_id"),
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.request.GET.get("workspace_id"),
            company_id=self.request.GET.get("company_id"),
            position_id=self.request.GET.get("job_position_id"),
        )


class JobApplicationCreateView(
    LoginRequiredMixin, AppContextMixin, JobApplicationFormMixin, CreateView
):

    model = JobApplication
    template_name = "applications/job_application/create.html"
    fields = [
        "status",
        "date_applied",
        "emails",
        "documents",
    ]

    def form_valid(self, form):

        JobApplicationService.create(
            user=self.request.user,
            context=JobApplicationContext(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"],
                job_position_id=self.kwargs["job_position_id"],
                id=None
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return application_list_url(
            self.kwargs["workspace_id"],
            self.kwargs["company_id"],
            self.kwargs["job_position_id"]
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            position_id=self.kwargs["job_position_id"],
            company_id=self.kwargs["company_id"],
        )


class JobApplicationDetailView(LoginRequiredMixin, AppContextMixin, DetailView):

    model = JobApplication
    template_name = "applications/job_application/detail.html"
    context_object_name = "job_application"

    @property
    def application(self):

        return self.object

    def get_queryset(self):

        return JobApplicationSelector.list(user=self.request.user)

    def get_object(self, queryset=None):

        return get_object_or_404(
            JobApplication, owner=self.request.user, pk=self.kwargs["pk"]
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
        )


class JobApplicationUpdateView(
    LoginRequiredMixin, AppContextMixin, JobApplicationFormMixin, UpdateView
):

    model = JobApplication
    template_name = "applications/job_application/edit.html"
    fields = [
        "status",
        "date_applied",
        "emails",
        "documents",
    ]

    @property
    def application(self):

        return self.object

    def get_queryset(self):

        return JobApplicationSelector.list(user=self.request.user)

    def form_valid(self, form):

        JobApplicationService.update(
            user=self.request.user,
            context=JobApplicationContext(
                workspace_id=self.application.workspace.workspace_id,
                company_id=self.application.job_position.company.pk,
                job_position_id=self.application.job_position.pk,
                id=self.application.pk,
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "job-application-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
        )


class JobApplicationDeleteView(LoginRequiredMixin, AppContextMixin, DeleteView):

    model = JobApplication
    template_name = "applications/job_application/delete.html"

    @property
    def application(self):

        return self.object

    def get_queryset(self):

        return JobApplicationSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        JobApplicationService.remove(
            user=self.request.user,
            context=JobApplicationContext(
                workspace_id=self.application.workspace.workspace_id,
                company_id=self.application.job_position.company.pk,
                job_position_id=self.application.job_position.pk,
                id=self.application.pk,
            )
        )

        return redirect(
            application_list_url(
                self.application.job_position.company.workspace_id,
                self.application.job_position.company_id,
                self.application.job_position_id,
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
        )
