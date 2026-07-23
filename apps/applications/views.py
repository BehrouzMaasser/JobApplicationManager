from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Models
from apps.applications.models import (
    JobApplication,
    JobApplicationNote
)
from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector
)

# Selectors
from apps.applications.selectors.application_selector import JobApplicationSelector
from apps.applications.services.application_note_service import (
    JobApplicationNoteService
)

# Services
from apps.applications.services.application_service import JobApplicationService

# Contexts
from apps.core.common.contexts.contexts import (
    JobApplicationContext,
    JobApplicationChildContext
)
from apps.core.common.types.filters import JobApplicationQueryFilter, \
    JobApplicationNoteQueryFilter

# View Contexts and Mixins
from apps.core.contexts.app_context import AppContext
from apps.core.contexts.extra_context import ExtraContext
from apps.core.mixins.app_context_mixin import AppContextMixin
from apps.core.mixins.job_application_form_mixin import JobApplicationFormMixin
from apps.core.mixins.service_validation_error_mixin import ServiceFormErrorMixin
from apps.core.mixins.view_exception_handler import ViewExceptionHandlerMixin


def application_list_url(workspace_id=None, company_id=None, job_position_id=None):

    params = {
        "workspace_id": workspace_id,
        "company_id": company_id,
        "job_position_id": job_position_id,
    }

    params = {param: value for param, value in params.items() if value is not None}

    return f"{reverse('job-application-list-web')}?{urlencode(params)}"


def application_note_list_url(
        workspace_id=None,
        company_id=None,
        job_position_id=None,
        job_application_id=None,
):

    params = {
        "workspace_id": workspace_id,
        "company_id": company_id,
        "job_position_id": job_position_id,
        "job_application_id": job_application_id,
    }

    params = {param: value for param, value in params.items() if value is not None}

    return f"{reverse('job-application-note-list-web')}?{urlencode(params)}"


class JobApplicationListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = JobApplication
    template_name = "applications/job_application/list.html"
    context_object_name = "job_applications"

    def get_queryset(self):

        return JobApplicationSelector.list(
            user=self.request.user,
            filters=JobApplicationQueryFilter(
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
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    JobApplicationFormMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = JobApplication
    template_name = "create_page.html"
    fields = [
        "status",
        "date_applied",
        "emails",
        "documents",
    ]

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobApplicationService.create(
                user=self.request.user,
                context=JobApplicationContext(
                    workspace_id=self.kwargs["workspace_id"],
                    company_id=self.kwargs["company_id"],
                    job_position_id=self.kwargs["job_position_id"],
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

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

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application",
            page_title="Create Job Application",
        )


class JobApplicationDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = JobApplication
    template_name = "applications/job_application/detail.html"
    context_object_name = "job_application"

    @property
    def application(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
            application_notes_list_url=application_note_list_url(
                job_application_id=self.application.pk
            )
        )


class JobApplicationUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    JobApplicationFormMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = JobApplication
    template_name = "edit_page.html"
    fields = [
        "status",
        "date_applied",
        "emails",
        "documents",
    ]

    @property
    def application(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobApplicationService.update(
                user=self.request.user,
                context=JobApplicationContext(
                    workspace_id=self.application.workspace.workspace_id,
                    company_id=self.application.job_position.company.pk,
                    job_position_id=self.application.job_position.pk,
                    id=self.application.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "job-application-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application",
            page_title="Update Job Application",
        )


class JobApplicationDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = JobApplication
    template_name = "delete_confirm.html"

    @property
    def application(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

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
            reverse(
                "job-position-detail-web",
                kwargs={"pk": self.application.job_position.pk}
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.application.workspace.workspace_id,
            company_id=self.application.job_position.company.pk,
            position_id=self.application.job_position.pk,
            application_id=self.application.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application",
            page_title="Delete Job Application",
        )


class JobApplicationNoteListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = JobApplicationNote
    template_name = "applications/application_note/list.html"
    context_object_name = "application_notes"

    def get_queryset(self):

        return JobApplicationNoteSelector.list(
            user=self.request.user,
            filters=JobApplicationNoteQueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
                company_id=self.request.GET.get("company_id"),
                job_position_id=self.request.GET.get("job_position_id"),
                job_application_id=self.request.GET.get("job_application_id"),
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.request.GET.get("workspace_id"),
            company_id=self.request.GET.get("company_id"),
            position_id=self.request.GET.get("job_position_id"),
            application_id=self.request.GET.get("job_application_id"),
        )


class JobApplicationNoteCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = JobApplicationNote
    template_name = "create_page.html"
    fields = ["title", "content"]

    @property
    def job_application(self):

        return JobApplicationSelector.get(
            user=self.request.user, obj_id=self.kwargs["job_application_id"]
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobApplicationNoteService.create(
                user=self.request.user,
                context=JobApplicationChildContext(
                    workspace_id=self.job_application.workspace.workspace_id,
                    company_id=self.job_application.job_position.company.pk,
                    job_position_id=self.job_application.job_position.pk,
                    job_application_id=self.job_application.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse(
            "job-application-detail-web",
            kwargs={
                "pk": self.kwargs["job_application_id"]
            }
        )

    def build_app_context(self):

        return AppContext(
            application_id=self.kwargs["job_application_id"],
            application_notes_list_url=application_note_list_url(
                job_application_id=self.kwargs["job_application_id"],
            )
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application note",
            page_title="Create Job Application Note",
        )


class JobApplicationNoteDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = JobApplicationNote
    template_name = "applications/application_note/detail.html"
    context_object_name = "application_note"

    @property
    def app_note(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.app_note.job_application.workspace.workspace_id,
            company_id=self.app_note.job_application.job_position.company.pk,
            position_id=self.app_note.job_application.job_position.pk,
            application_id=self.app_note.job_application.pk,
            application_note_id=self.app_note.pk
        )


class JobApplicationNoteUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = JobApplicationNote
    template_name = "edit_page.html"
    fields = ["title", "content"]

    @property
    def app_note(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobApplicationNoteService.update(
                user=self.request.user,
                context=JobApplicationChildContext(
                    workspace_id=self.app_note.job_application.workspace.workspace_id,
                    company_id=self.app_note.job_application.job_position.company.pk,
                    job_position_id=self.app_note.job_application.job_position.pk,
                    job_application_id=self.app_note.job_application.pk,
                    id=self.app_note.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "job-application-detail-web",
            kwargs={
                "pk": self.app_note.job_application.pk,
            }
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.app_note.job_application.workspace.workspace_id,
            company_id=self.app_note.job_application.job_position.company.pk,
            position_id=self.app_note.job_application.job_position.pk,
            application_id=self.app_note.job_application.pk,
            application_note_id=self.app_note.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application note",
            page_title="Update Job Application Note",
        )


class JobApplicationNoteDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = JobApplicationNote
    template_name = "delete_confirm.html"

    @property
    def app_note(self):

        return self.object

    def get_object(self, queryset=None):

        return JobApplicationNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"]
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        JobApplicationNoteService.remove(
            user=self.request.user,
            context=JobApplicationChildContext(
                workspace_id=self.app_note.job_application.workspace.workspace_id,
                company_id=self.app_note.job_application.job_position.company.pk,
                job_position_id=self.app_note.job_application.job_position.pk,
                job_application_id=self.app_note.job_application.pk,
                id=self.kwargs["pk"],
            )
        )

        return redirect(
            "job-application-detail-web",
            pk=self.app_note.job_application.pk,
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.app_note.job_application.workspace.workspace_id,
            company_id=self.app_note.job_application.job_position.company.pk,
            position_id=self.app_note.job_application.job_position.pk,
            application_id=self.app_note.job_application.pk,
            application_note_id=self.app_note.pk
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job application note",
            page_title="Delete Job Application Note",
        )
