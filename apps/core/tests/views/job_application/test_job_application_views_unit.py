import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse, Http404
from django.test import RequestFactory

from apps.applications.views import (
    JobApplicationListView,
    JobApplicationCreateView,
    JobApplicationDetailView,
    JobApplicationUpdateView,
    JobApplicationDeleteView,
)

from apps.applications.views import (
    JobApplicationContext,
)
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)

pytestmark = pytest.mark.django_db


class TestJobApplicationListView:

    @patch(
        "apps.applications.views.JobApplicationSelector.list"
    )
    def test_get_queryset_calls_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()

        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
                "company_id": "1",
                "job_position_id": "2",
            },
        )

        request.user = user1

        view = JobApplicationListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1

        assert (
            kwargs["filters"].workspace_id
            == "workspace-id"
        )

        assert (
            kwargs["filters"].company_id
            == "1"
        )

        assert (
            kwargs["filters"].job_position_id
            == "2"
        )

        assert result is queryset

    @patch("apps.applications.views.JobApplicationSelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(
        self,
        mock_list,
        user1,
    ):
        mock_list.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
                "company_id": "1",
                "job_position_id": "2",
            },
        )

        request.user = user1

        view = JobApplicationListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)

    def test_build_app_context(
        self,
        user1,
    ):
        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
                "company_id": "1",
                "job_position_id": "2",
            },
        )

        request.user = user1

        view = JobApplicationListView()
        view.request = request

        context = view.build_app_context()

        assert context.workspace_id == "workspace-id"
        assert context.company_id == "1"
        assert context.position_id == "2"


class TestJobApplicationCreateView:

    @patch(
        "apps.applications.views.redirect"
    )
    @patch(
        "apps.applications.views.JobApplicationService.create"
    )
    def test_form_valid_calls_service(
        self,
        mock_create,
        mock_redirect,
        user1,
    ):
        response = HttpResponse()

        mock_redirect.return_value = response

        form = Mock()

        form.cleaned_data = {
            "status": "APPLIED",
        }

        request = RequestFactory().post("/")

        request.user = user1

        view = JobApplicationCreateView()

        view.request = request

        view.kwargs = {
            "workspace_id": "workspace-id",
            "company_id": 1,
            "job_position_id": 2,
        }

        result = view.form_valid(form)

        mock_create.assert_called_once()

        kwargs = mock_create.call_args.kwargs

        assert kwargs["user"] == user1

        assert kwargs["validated_data"] == (
            form.cleaned_data
        )

        assert isinstance(
            kwargs["context"],
            JobApplicationContext,
        )

        assert (
            kwargs["context"].workspace_id
            == "workspace-id"
        )

        assert (
            kwargs["context"].company_id
            == 1
        )

        assert (
            kwargs["context"].job_position_id
            == 2
        )

        assert kwargs["context"].id is None

        mock_redirect.assert_called_once()

        assert result is response

    @patch("apps.applications.views.JobApplicationService.create")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_create,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["status"]
        err.messages = ["invalid status"]
        mock_create.side_effect = err

        form = Mock()
        form.cleaned_data = {"status": "BAD"}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobApplicationCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
            "company_id": 1,
            "job_position_id": 2,
        }

        result = view.form_valid(form)

        form.add_error.assert_called_with("status", "invalid status")
        assert hasattr(result, "status_code")
        assert result.status_code == 200

    def test_get_success_url(self):

        view = JobApplicationCreateView()

        view.kwargs = {
            "workspace_id": "workspace-id",
            "company_id": 1,
            "job_position_id": 2,
        }

        url = view.get_success_url()

        assert (
            "workspace_id=workspace-id"
            in url
        )

        assert (
            "company_id=1"
            in url
        )

        assert (
            "job_position_id=2"
            in url
        )

    def test_build_app_context(self):

        view = JobApplicationCreateView()

        view.kwargs = {
            "workspace_id": "workspace-id",
            "company_id": 1,
            "job_position_id": 2,
        }

        context = view.build_app_context()

        assert context.workspace_id == "workspace-id"
        assert context.company_id == 1
        assert context.position_id == 2

    def test_build_extra_context(self):

        view = JobApplicationCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "job application"

        assert (
            context.page_title
            == "Create Job Application"
        )


class TestJobApplicationDetailView:

    @patch(
        "apps.applications.views.JobApplicationSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_application1,
    ):
        mock_get.return_value = job_application1

        request = RequestFactory().get("/")

        request.user = user1

        view = JobApplicationDetailView()

        view.request = request

        view.kwargs = {
            "pk": job_application1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_application1.pk,
        )

        assert result is job_application1

    @patch("apps.applications.views.JobApplicationSelector.get")
    def test_dispatch_translates_selector_get_exceptions_to_404(
        self,
        mock_get,
        user1,
    ):
        mock_get.side_effect = ResourceNotFoundError("missing")

        request = RequestFactory().get("/")
        request.user = user1

        view = JobApplicationDetailView()
        view.request = request
        view.kwargs = {
            "pk": "123",
        }

        with pytest.raises(Http404):
            view.dispatch(request)

    def test_build_app_context(
        self,
        job_application1,
    ):
        view = JobApplicationDetailView()

        view.object = job_application1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == job_application1.workspace.workspace_id
        )

        assert (
            context.company_id
            == job_application1.job_position.company.pk
        )

        assert (
            context.position_id
            == job_application1.job_position.pk
        )

        assert (
            context.application_id
            == job_application1.pk
        )

        assert (
            context.application_notes_list_url
            is not None
        )


class TestJobApplicationUpdateView:

    @patch(
        "apps.applications.views.JobApplicationSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_application1,
    ):
        mock_get.return_value = job_application1

        request = RequestFactory().get("/")

        request.user = user1

        view = JobApplicationUpdateView()

        view.request = request

        view.kwargs = {
            "pk": job_application1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_application1.pk,
        )

        assert result is job_application1

    @patch(
        "apps.applications.views.redirect"
    )
    @patch(
        "apps.applications.views.JobApplicationService.update"
    )
    def test_form_valid_calls_service(
        self,
        mock_update,
        mock_redirect,
        user1,
        job_application1,
    ):
        response = HttpResponse()

        mock_redirect.return_value = response

        form = Mock()

        form.cleaned_data = {
            "status": "INTERVIEW",
        }

        request = RequestFactory().post("/")

        request.user = user1

        view = JobApplicationUpdateView()

        view.request = request

        view.object = job_application1

        view.kwargs = {
            "pk": job_application1.pk,
        }

        result = view.form_valid(form)

        mock_update.assert_called_once()

        kwargs = mock_update.call_args.kwargs

        assert kwargs["user"] == user1

        assert (
            kwargs["validated_data"]
            == form.cleaned_data
        )

        assert (
            kwargs["context"].workspace_id
            == job_application1.workspace.workspace_id
        )

        assert (
            kwargs["context"].company_id
            == job_application1.job_position.company.pk
        )

        assert (
            kwargs["context"].job_position_id
            == job_application1.job_position.pk
        )

        assert (
            kwargs["context"].id
            == job_application1.pk
        )

        mock_redirect.assert_called_once()

        assert result is response

    def test_get_success_url(
        self,
        job_application1,
    ):
        view = JobApplicationUpdateView()

        view.kwargs = {
            "pk": job_application1.pk,
        }

        url = view.get_success_url()

        assert (
            str(job_application1.pk)
            in url
        )

    def test_build_app_context(
        self,
        job_application1,
    ):
        view = JobApplicationUpdateView()

        view.object = job_application1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == job_application1.workspace.workspace_id
        )

        assert (
            context.company_id
            == job_application1.job_position.company.pk
        )

        assert (
            context.position_id
            == job_application1.job_position.pk
        )

        assert (
            context.application_id
            == job_application1.pk
        )

    def test_build_extra_context(self):

        view = JobApplicationUpdateView()

        context = view.build_extra_context()

        assert (
            context.app_kind
            == "job application"
        )

        assert (
            context.page_title
            == "Update Job Application"
        )


class TestJobApplicationDeleteView:

    @patch(
        "apps.applications.views.JobApplicationSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        job_application1,
    ):
        mock_get.return_value = job_application1

        request = RequestFactory().get("/")

        request.user = user1

        view = JobApplicationDeleteView()

        view.request = request

        view.kwargs = {
            "pk": job_application1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=job_application1.pk,
        )

        assert result is job_application1


    @patch(
        "apps.applications.views.redirect"
    )
    @patch(
        "apps.applications.views.JobApplicationService.remove"
    )
    @patch(
        "apps.applications.views.JobApplicationSelector.get"
    )
    def test_post_calls_remove_service(
        self,
        mock_get,
        mock_remove,
        mock_redirect,
        user1,
        job_application1,
    ):
        response = HttpResponse()

        mock_get.return_value = job_application1

        mock_redirect.return_value = response

        request = RequestFactory().post("/")

        request.user = user1

        view = JobApplicationDeleteView()

        view.request = request

        view.kwargs = {
            "pk": job_application1.pk,
        }

        result = view.post(
            request,
            pk=job_application1.pk,
        )

        mock_remove.assert_called_once()

        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == user1

        assert (
            kwargs["context"].workspace_id
            == job_application1.workspace.workspace_id
        )

        assert (
            kwargs["context"].company_id
            == job_application1.job_position.company.pk
        )

        assert (
            kwargs["context"].job_position_id
            == job_application1.job_position.pk
        )

        assert (
            kwargs["context"].id
            == job_application1.pk
        )

        mock_redirect.assert_called_once()

        assert result is response

    def test_build_app_context(
        self,
        job_application1,
    ):
        view = JobApplicationDeleteView()

        view.object = job_application1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == job_application1.workspace.workspace_id
        )

        assert (
            context.company_id
            == job_application1.job_position.company.pk
        )

        assert (
            context.position_id
            == job_application1.job_position.pk
        )

        assert (
            context.application_id
            == job_application1.pk
        )

    def test_build_extra_context(self):

        view = JobApplicationDeleteView()

        context = view.build_extra_context()

        assert (
            context.app_kind
            == "job application"
        )

        assert (
            context.page_title
            == "Delete Job Application"
        )
