from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.urls import reverse

# Models
from .models import Company, CompanyEmail, CompanyNote, JobPosition

# Selectors
from .selectors.company_email_selector import CompanyEmailSelector
from .selectors.company_note_selector import CompanyNoteSelector
from .selectors.company_selector import CompanySelector
from .selectors.job_position_selector import JobPositionSelector

# Services
from .services.company_email_service import CompanyEmailService
from .services.company_note_service import CompanyNoteService
from .services.company_service import CompanyService

from apps.core.common.contexts.contexts import (
    CompanyContext,
    CompanyChildContext
)
from .services.job_position_service import JobPositionService
from ..applications.views import application_list_url
from ..core.common.types.filters import (
    CompanyQueryFilter,
    CompanyEmailQueryFilter,
    CompanyNoteQueryFilter,
    JobPositionQueryFilter
)

# View Contexts and Mixins
from ..core.view_contexts.app_context import AppContext
from ..core.view_contexts.extra_context import ExtraContext
from ..core.mixins.app_context_mixin import AppContextMixin
from apps.companies.mixins.jop_position_form_mixin import JobPositionFormMixin
from ..core.mixins.service_validation_error_mixin import ServiceFormErrorMixin
from apps.companies.mixins.create_view_context_validation_mixins import (
    CompanyChildCreateViewContextValidationMixin,
    WorkspaceChildCreateViewContextValidationMixin
)
from ..core.mixins.view_exception_handler import ViewExceptionHandlerMixin


def company_list_url(workspace_id=None):

    if workspace_id:
        params = {
            "workspace_id": workspace_id,
        }
    else:
        params = {}

    return f"{reverse('company-list-web')}?{urlencode(params)}"


def position_list_url(workspace_id=None, company_id=None):

    params = {
        "workspace_id": workspace_id,
        "company_id": company_id,
    }

    params = {key: value for key, value in params.items() if value is not None}

    return f"{reverse('job-position-list-web')}?{urlencode(params)}"


def company_note_list_url(workspace_id=None, company_id=None):

    params = {
        "workspace_id": workspace_id,
        "company_id": company_id,
    }

    params = {key: value for key, value in params.items() if value is not None}

    return f"{reverse('company-note-list-web')}?{urlencode(params)}"


def company_email_list_url(workspace_id=None, company_id=None):

    params = {
        "workspace_id": workspace_id,
        "company_id": company_id,
    }

    params = {key: value for key, value in params.items() if value is not None}

    return f"{reverse('company-email-list-web')}?{urlencode(params)}"


class CompanyListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = Company
    template_name = "companies/company/list.html"
    context_object_name = "companies"

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=CompanyQueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.request.GET.get("workspace_id"),
        )


class CompanyCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    WorkspaceChildCreateViewContextValidationMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = Company
    template_name = "create_page.html"
    fields = ["name", "website"]

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyService.create(
                user=self.request.user,
                context=CompanyContext(
                    workspace_id=self.kwargs["workspace_id"],
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return company_list_url(self.kwargs["workspace_id"])

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            companies_list_url=company_list_url(
                workspace_id=self.kwargs["workspace_id"]
            )
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company",
            page_title="Create Company",
        )


class CompanyDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = Company
    template_name = "companies/company/detail.html"
    context_object_name = "company"

    @property
    def company(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanySelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def build_app_context(self):

        companies_list_url = company_list_url(
            workspace_id=self.company.workspace.workspace_id
        )

        company_emails_list_url = company_email_list_url(
            company_id=self.company.pk
        )

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
            applications_list_url=application_list_url(company_id=self.company.pk),
            companies_list_url=companies_list_url,
            positions_list_url=position_list_url(company_id=self.company.pk),
            company_emails_list_url=company_emails_list_url,
            company_notes_list_url=company_note_list_url(company_id=self.company.pk),
        )


class CompanyUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = Company
    template_name = "edit_page.html"
    fields = ["name", "website"]

    @property
    def company(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanySelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyService.update(
                user=self.request.user,
                context=CompanyContext(
                    workspace_id=self.company.workspace.workspace_id,
                    id=self.company.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
            companies_list_url=company_list_url(
                workspace_id=self.company.workspace.workspace_id
            )
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company",
            page_title="Update Company",
        )


class CompanyDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = Company
    template_name = "delete_confirm.html"

    @property
    def company(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanySelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        CompanyService.remove(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=self.company.workspace.workspace_id,
                id=self.company.pk,
            )
        )

        return redirect(
            company_list_url(workspace_id=self.company.workspace.workspace_id)
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
            companies_list_url=company_list_url(
                workspace_id=self.company.workspace.workspace_id
            )
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company",
            page_title="Delete Company",
        )


class CompanyEmailListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = CompanyEmail
    template_name = "companies/email/list.html"
    context_object_name = "emails"

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailQueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
                company_id=self.request.GET.get("company_id")
            )
        )

    def build_app_context(self):

        workspace_id = self.request.GET.get("workspace_id")
        company_id = self.request.GET.get("company_id")

        company = CompanySelector.list(
            user=self.request.user,
            filters=CompanyQueryFilter(
                id=company_id
            )
        ).first()

        if company:
            workspace_id = company.workspace.workspace_id
            company_id = company.pk

        return AppContext(
            workspace_id=workspace_id,
            company_id=company_id,
        )


class CompanyEmailCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    CompanyChildCreateViewContextValidationMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = CompanyEmail
    template_name = "create_page.html"
    fields = ["title", "email"]

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyEmailService.create(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.kwargs["workspace_id"],
                    company_id=self.kwargs["company_id"],
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.kwargs["company_id"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company email",
            page_title="Create Company Email",
        )


class CompanyEmailDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = CompanyEmail
    template_name = "companies/email/detail.html"
    context_object_name = "email"

    @property
    def email(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyEmailSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.email.company.workspace.workspace_id,
            company_id=self.email.company.pk,
            email_id=self.email.pk,
        )


class CompanyEmailUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = CompanyEmail
    template_name = "edit_page.html"
    fields = ["title", "email"]

    @property
    def email(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyEmailSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyEmailService.update(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.email.company.workspace.workspace_id,
                    company_id=self.email.company.pk,
                    id=self.email.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.email.company.pk}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.email.company.workspace.workspace_id,
            company_id=self.email.company.pk,
            email_id=self.email.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company email",
            page_title="Update Company Email",
        )


class CompanyEmailDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = CompanyEmail
    template_name = "delete_confirm.html"

    @property
    def email(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyEmailSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        CompanyEmailService.remove(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.email.company.workspace.workspace_id,
                company_id=self.email.company.pk,
                id=self.email.pk,
            )
        )

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse(
            "company-detail-web",
            kwargs={"pk": self.email.company.pk}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.email.company.workspace.workspace_id,
            company_id=self.email.company.pk,
            email_id=self.email.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company email",
            page_title="Delete Company Email",
        )


class CompanyNoteListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = CompanyNote
    template_name = "companies/note/list.html"
    context_object_name = "notes"

    def get_queryset(self):

        return CompanyNoteSelector.list(
            user=self.request.user,
            filters=CompanyNoteQueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
                company_id=self.request.GET.get("company_id"),
            )
        )

    def build_app_context(self):

        workspace_id = self.request.GET.get("workspace_id")
        company_id = self.request.GET.get("company_id")

        company = CompanySelector.list(
            user=self.request.user,
            filters=CompanyQueryFilter(
                id=company_id
            )
        ).first()

        if company:
            workspace_id = company.workspace.workspace_id
            company_id = company.pk

        return AppContext(
            workspace_id=workspace_id,
            company_id=company_id,
        )


class CompanyNoteCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    CompanyChildCreateViewContextValidationMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = CompanyNote
    template_name = "create_page.html"
    fields = ["title", "content"]

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyNoteService.create(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.kwargs["workspace_id"],
                    company_id=self.kwargs["company_id"],
                    id=None
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.kwargs["company_id"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company note",
            page_title="Create Company Note",
        )


class CompanyNoteDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = CompanyNote
    template_name = "companies/note/detail.html"
    context_object_name = "note"

    @property
    def company_note(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company_note.company.workspace.workspace_id,
            company_id=self.company_note.company.pk,
            note_id=self.company_note.pk,
        )


class CompanyNoteUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = CompanyNote
    template_name = "edit_page.html"
    fields = ["title", "content"]

    @property
    def company_note(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: CompanyNoteService.update(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.company_note.company.workspace.workspace_id,
                    company_id=self.company_note.company.pk,
                    id=self.company_note.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.company_note.company.pk}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company_note.company.workspace.workspace_id,
            company_id=self.company_note.company.pk,
            note_id=self.company_note.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company note",
            page_title="Update Company Note",
        )


class CompanyNoteDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = CompanyNote
    template_name = "delete_confirm.html"

    @property
    def company_note(self):

        return self.object

    def get_object(self, queryset=None):

        return CompanyNoteSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        CompanyNoteService.remove(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.company_note.company.workspace.workspace_id,
                company_id=self.company_note.company.pk,
                id=self.company_note.pk,
            )
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.company_note.company.pk}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company_note.company.workspace.workspace_id,
            company_id=self.company_note.company.pk,
            note_id=self.company_note.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="company note",
            page_title="Delete Company Note",
        )


class JobPositionListView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, ListView
):

    model = JobPosition
    template_name = "companies/job_position/list.html"
    context_object_name = "job_positions"

    def get_queryset(self):

        return JobPositionSelector.list(
            user=self.request.user,
            filters=JobPositionQueryFilter(
                workspace_id=self.request.GET.get("workspace_id"),
                company_id=self.request.GET.get("company_id"),
            )
        )

    def build_app_context(self):

        company_id = self.request.GET.get("company_id")
        workspace_id = self.request.GET.get("workspace_id")

        company = CompanySelector.list(
            user=self.request.user,
            filters=CompanyQueryFilter(
                id=self.request.GET.get("company_id")
            )
        ).first()

        if company:
            workspace_id = company.workspace.workspace_id
            company_id = company.pk

        return AppContext(
            workspace_id=workspace_id,
            company_id=company_id,
        )


class JobPositionCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    CompanyChildCreateViewContextValidationMixin,
    AppContextMixin,
    JobPositionFormMixin,
    ServiceFormErrorMixin,
    CreateView
):

    model = JobPosition
    template_name = "create_page.html"
    fields = [
        "title",
        "description",
        "employment_types",
        "job_sites",
        "tasks",
        "requirements",
        "benefits",
        "date_posted",
        "min_salary",
        "max_salary",
        "job_position_ad_url",
        "job_location_url",
        "job_portal_url",
        "portal_username",
        "portal_password",
    ]

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobPositionService.create(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.kwargs["workspace_id"],
                    company_id=self.kwargs["company_id"],
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.kwargs["company_id"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job position",
            page_title="Create Job Position",
        )


class JobPositionDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = JobPosition
    template_name = "companies/job_position/detail.html"
    context_object_name = "job_position"

    @property
    def job_position(self):

        return self.object

    def get_object(self, queryset=None):

        return JobPositionSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.job_position.company.workspace.workspace_id,
            company_id=self.job_position.company.pk,
            position_id=self.job_position.pk,
            applications_list_url=application_list_url(
                workspace_id=self.job_position.company.workspace.workspace_id,
                company_id=self.job_position.company.pk,
                job_position_id=self.job_position.pk,
            )
        )


class JobPositionUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    JobPositionFormMixin,
    ServiceFormErrorMixin,
    UpdateView
):

    model = JobPosition
    template_name = "edit_page.html"
    fields = [
        "title",
        "description",
        "employment_types",
        "job_sites",
        "tasks",
        "requirements",
        "benefits",
        "date_posted",
        "min_salary",
        "max_salary",
        "job_position_ad_url",
        "job_location_url",
        "job_portal_url",
        "portal_username",
        "portal_password",
    ]

    @property
    def job_position(self):

        return self.object

    def get_object(self, queryset=None):

        return JobPositionSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def form_valid(self, form):

        response = self.execute_service(
            form=form,
            operation=lambda: JobPositionService.update(
                user=self.request.user,
                context=CompanyChildContext(
                    workspace_id=self.job_position.company.workspace.workspace_id,
                    company_id=self.job_position.company.pk,
                    id=self.job_position.pk,
                ),
                validated_data=form.cleaned_data
            )
        )

        if response:
            return response

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "job-position-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.job_position.company.workspace.workspace_id,
            company_id=self.job_position.company.pk,
            position_id=self.job_position.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job position",
            page_title="Update Job Position",
        )


class JobPositionDeleteView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    DeleteView
):

    model = JobPosition
    template_name = "delete_confirm.html"

    @property
    def job_position(self):

        return self.object

    def get_object(self, queryset=None):

        return JobPositionSelector.get(
            user=self.request.user, obj_id=self.kwargs["pk"],
        )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        JobPositionService.remove(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.job_position.company.workspace.workspace_id,
                company_id=self.job_position.company.pk,
                id=self.job_position.pk,
            )
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "job-position-detail-web",
            kwargs={"pk": self.job_position.company.pk}
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.job_position.company.workspace.workspace_id,
            company_id=self.job_position.company.pk,
            position_id=self.job_position.pk,
        )

    def build_extra_context(self):

        return ExtraContext(
            app_kind="job position",
            page_title="Delete Job Position",
        )
