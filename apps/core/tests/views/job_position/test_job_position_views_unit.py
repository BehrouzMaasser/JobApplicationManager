import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse, Http404
from django.test import RequestFactory

from apps.companies.views import (
    JobPositionListView,
    JobPositionCreateView,
    JobPositionDetailView, JobPositionDeleteView, JobPositionUpdateView,
)

from apps.core.common.contexts.contexts import CompanyChildContext
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)

pytestmark = pytest.mark.django_db


class TestJobPositionListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.JobPositionSelector.list")
    def test_get_queryset_calls_selector_with_expected_filters(
        self,
        mock_list,
        user1,
        job_position1_user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "company_id": job_position1_user1.company.pk,
            },
        )
        request.user = user1

        view = JobPositionListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["filters"].company_id == str(
            job_position1_user1.company.pk
        )

        assert result is queryset

    @patch("apps.companies.views.JobPositionSelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(
        self,
        mock_list,
        user1,
    ):
        mock_list.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().get(
            "/",
            {
                "company_id": "123",
            },
        )
        request.user = user1

        view = JobPositionListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)

    # ------------------------
    # App Context
    # ------------------------

    @patch("apps.companies.views.CompanySelector.list")
    def test_build_app_context_uses_company_when_found(
        self,
        mock_list,
        user1,
        co1_ws1_user1,
    ):
        mock_queryset = Mock()
        mock_queryset.first.return_value = co1_ws1_user1
        mock_list.return_value = mock_queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": co1_ws1_user1.workspace.workspace_id,
                "company_id": co1_ws1_user1.pk,
            },
        )
        request.user = user1

        view = JobPositionListView()
        view.request = request

        context = view.build_app_context()

        mock_list.assert_called_once()

        assert context.workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )
        assert context.company_id == co1_ws1_user1.pk

    @patch("apps.companies.views.CompanySelector.list")
    def test_build_app_context_falls_back_to_query_parameters(
        self,
        mock_list,
        user1,
        workspace1_user1,
    ):
        mock_queryset = Mock()
        mock_queryset.first.return_value = None
        mock_list.return_value = mock_queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": workspace1_user1.workspace_id,
                "company_id": "123",
            },
        )
        request.user = user1

        view = JobPositionListView()
        view.request = request

        context = view.build_app_context()

        assert context.workspace_id == str(
            workspace1_user1.workspace_id
        )
        assert context.company_id == "123"


class TestJobPositionCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch.object(JobPositionCreateView, "execute_service")
    @patch("apps.companies.views.redirect")
    def test_form_valid_executes_service_and_redirects(
        self,
        mock_redirect,
        mock_execute_service,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_execute_service.return_value = None
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "Backend Developer",
            "description": "Description",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        kwargs = mock_execute_service.call_args.kwargs

        assert kwargs["form"] is form

        with patch("apps.companies.views.JobPositionService.create") as mock_create:
            kwargs["operation"]()

            mock_create.assert_called_once_with(
                user=user1,
                context=CompanyChildContext(
                    workspace_id=co1_ws1_user1.workspace.workspace_id,
                    company_id=co1_ws1_user1.pk,
                ),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once()

        assert result is response

    @patch("apps.companies.views.JobPositionService.create")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_create,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["title"]
        err.messages = ["invalid title"]
        mock_create.side_effect = err

        form = Mock()
        form.cleaned_data = {"title": "Bad", "description": ""}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionCreateView()
        view.request = request
        view.kwargs = {"workspace_id": "workspace-id", "company_id": "1"}

        result = view.form_valid(form)

        form.add_error.assert_called_with("title", "invalid title")
        assert hasattr(result, "status_code")
        assert result.status_code == 200

    @patch.object(JobPositionCreateView, "execute_service")
    def test_form_valid_returns_execute_service_response(
        self,
        mock_execute_service,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse(status=400)

        mock_execute_service.return_value = response

        form = Mock()
        form.cleaned_data = {}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co1_ws1_user1,
    ):
        view = JobPositionCreateView()

        view.kwargs = {
            "company_id": co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        view = JobPositionCreateView()

        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        context = view.build_app_context()

        assert context.workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )
        assert context.company_id == co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = JobPositionCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "job position"
        assert context.page_title == "Create Job Position"


class TestJobPositionDetailView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.JobPositionSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_position1_user1,
    ):
        mock_get.return_value = job_position1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = JobPositionDetailView()
        view.request = request
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        job_position1_user1,
    ):
        view = JobPositionDetailView()
        view.object = job_position1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert context.company_id == (
            job_position1_user1.company.pk
        )

        assert context.position_id == (
            job_position1_user1.pk
        )

        assert context.applications_list_url is not None
        assert context.companies_list_url is None
        assert context.positions_list_url is None
        assert context.company_emails_list_url is None
        assert context.company_notes_list_url is None


class TestJobPositionUpdateView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.JobPositionSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_position1_user1,
    ):
        mock_get.return_value = job_position1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = JobPositionUpdateView()
        view.request = request
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch.object(JobPositionUpdateView, "execute_service")
    @patch("apps.companies.views.redirect")
    def test_form_valid_executes_service_and_redirects(
        self,
        mock_redirect,
        mock_execute_service,
        user1,
        job_position1_user1,
    ):
        response = HttpResponse()

        mock_execute_service.return_value = None
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "Updated",
            "description": "Updated",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionUpdateView()
        view.request = request
        view.object = job_position1_user1
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        kwargs = mock_execute_service.call_args.kwargs

        assert kwargs["form"] is form

        with patch("apps.companies.views.JobPositionService.update") as mock_update:
            kwargs["operation"]()

            mock_update.assert_called_once_with(
                user=user1,
                context=CompanyChildContext(
                    workspace_id=job_position1_user1.company.workspace.workspace_id,
                    company_id=job_position1_user1.company.pk,
                    id=job_position1_user1.pk,
                ),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once()

        assert result is response

    @patch("apps.companies.views.JobPositionService.update")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_update,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["title"]
        err.messages = ["cannot use this title"]
        mock_update.side_effect = err

        form = Mock()
        form.cleaned_data = {"title": "Bad Update", "description": ""}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionUpdateView()
        view.request = request
        view.object = None
        view.kwargs = {"pk": "123"}

        result = view.form_valid(form)

        form.add_error.assert_called_with("title", "cannot use this title")
        assert hasattr(result, "status_code")
        assert result.status_code == 200

    @patch.object(JobPositionUpdateView, "execute_service")
    def test_form_valid_returns_execute_service_response(
        self,
        mock_execute_service,
        user1,
        job_position1_user1,
    ):
        response = HttpResponse(status=400)

        mock_execute_service.return_value = response

        form = Mock()
        form.cleaned_data = {}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionUpdateView()
        view.request = request
        view.object = job_position1_user1
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.form_valid(form)

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        job_position1_user1,
    ):
        view = JobPositionUpdateView()

        view.object = job_position1_user1
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        url = view.get_success_url()

        assert str(job_position1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        job_position1_user1,
    ):
        view = JobPositionUpdateView()
        view.object = job_position1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert context.company_id == (
            job_position1_user1.company.pk
        )

        assert context.position_id == (
            job_position1_user1.pk
        )

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = JobPositionUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "job position"
        assert context.page_title == "Update Job Position"


class TestJobPositionDeleteView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.JobPositionSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_position1_user1,
    ):
        mock_get.return_value = job_position1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = JobPositionDeleteView()
        view.request = request
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.JobPositionService.remove")
    @patch.object(JobPositionDeleteView, "get_object")
    def test_post_executes_remove_service_and_redirects(
        self,
        mock_get_object,
        mock_remove,
        mock_redirect,
        user1,
        job_position1_user1,
    ):
        response = HttpResponse()

        mock_get_object.return_value = job_position1_user1
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionDeleteView()
        view.request = request
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.post(request)

        mock_get_object.assert_called_once()

        mock_remove.assert_called_once_with(
            user=user1,
            context=CompanyChildContext(
                workspace_id=job_position1_user1.company.workspace.workspace_id,
                company_id=job_position1_user1.company.pk,
                id=job_position1_user1.pk,
            ),
        )

        mock_redirect.assert_called_once_with(
            view.get_success_url()
        )

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        job_position1_user1,
    ):
        view = JobPositionDeleteView()
        view.object = job_position1_user1

        url = view.get_success_url()

        assert str(job_position1_user1.company.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        job_position1_user1,
    ):
        view = JobPositionDeleteView()
        view.object = job_position1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert context.company_id == (
            job_position1_user1.company.pk
        )

        assert context.position_id == (
            job_position1_user1.pk
        )

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = JobPositionDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "job position"
        assert context.page_title == "Delete Job Position"
