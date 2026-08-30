import pytest
from unittest.mock import Mock, patch

from django.http import HttpResponse, Http404
from django.test import RequestFactory

from apps.applications.views import (
    JobApplicationNoteListView,
    JobApplicationNoteCreateView,
    JobApplicationNoteDetailView,
    JobApplicationNoteUpdateView,
    JobApplicationNoteDeleteView,
)
from apps.core.common.contexts.contexts import JobApplicationChildContext
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)

pytestmark = pytest.mark.django_db


class TestJobApplicationNoteListView:

    @patch("apps.applications.views.JobApplicationNoteSelector.list")
    def test_get_queryset_calls_selector(self, mock_list, user1):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
                "company_id": "1",
                "job_position_id": "2",
                "job_application_id": "3",
            },
        )
        request.user = user1

        view = JobApplicationNoteListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()
        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["filters"].workspace_id == "workspace-id"
        assert kwargs["filters"].company_id == "1"
        assert kwargs["filters"].job_position_id == "2"
        assert kwargs["filters"].job_application_id == "3"
        assert result is queryset

    @patch("apps.applications.views.JobApplicationNoteSelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(self, mock_list, user1):
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

        view = JobApplicationNoteListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)

    def test_build_app_context(self, user1):
        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
                "company_id": "1",
                "job_position_id": "2",
                "job_application_id": "3",
            },
        )
        request.user = user1

        view = JobApplicationNoteListView()
        view.request = request

        ctx = view.build_app_context()

        assert ctx.workspace_id == "workspace-id"
        assert ctx.company_id == "1"
        assert ctx.position_id == "2"
        assert ctx.application_id == "3"


class TestJobApplicationNoteCreateView:

    @patch("apps.applications.views.redirect")
    @patch("apps.applications.views.JobApplicationNoteService.create")
    @patch("apps.applications.views.JobApplicationSelector.get")
    def test_form_valid_calls_service(
            self, mock_get, mock_create, mock_redirect, user1, job_application1
    ):
        # Arrange
        mock_get.return_value = job_application1
        mock_create.return_value = None
        mock_redirect.return_value = HttpResponse()

        request = RequestFactory().post("/")
        request.user = job_application1.owner

        view = JobApplicationNoteCreateView()
        view.request = request
        view.kwargs = {"job_application_id": str(job_application1.pk)}

        form = Mock()
        form.cleaned_data = {"title": "T", "content": "C"}

        # Act
        result = view.form_valid(form)

        # Assert
        mock_get.assert_called_once_with(
            user=job_application1.owner, obj_id=str(job_application1.pk)
        )
        mock_create.assert_called_once()
        create_kwargs = mock_create.call_args.kwargs

        assert create_kwargs["user"] == job_application1.owner
        assert isinstance(create_kwargs["context"], JobApplicationChildContext)
        ctx = create_kwargs["context"]
        assert ctx.workspace_id == job_application1.workspace.workspace_id
        assert ctx.company_id == job_application1.job_position.company.pk
        assert ctx.job_position_id == job_application1.job_position.pk
        assert ctx.job_application_id == job_application1.pk
        assert create_kwargs["validated_data"] == form.cleaned_data

        mock_redirect.assert_called_once()
        assert result is mock_redirect.return_value

    @patch("apps.applications.views.JobApplicationNoteService.create")
    @patch("apps.applications.views.JobApplicationSelector.get")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
            self, mock_get, mock_create, job_application1
    ):
        mock_get.return_value = job_application1

        err = BusinessRuleViolationError()
        err.fields = ["title"]
        err.messages = ["invalid title"]
        mock_create.side_effect = err

        request = RequestFactory().post("/")
        request.user = job_application1.owner

        view = JobApplicationNoteCreateView()
        view.request = request
        view.kwargs = {"job_application_id": str(job_application1.pk)}
        view.object = Mock()

        form = Mock()
        form.cleaned_data = {"title": "bad", "content": "x"}

        result = view.form_valid(form)

        form.add_error.assert_called_with("title", "invalid title")
        assert result.status_code == 200

    def test_get_success_url(self, job_application1):
        view = JobApplicationNoteCreateView()
        view.kwargs = {"job_application_id": str(job_application1.pk)}

        url = view.get_success_url()
        assert f"applications/{job_application1.pk}/" in url

    def test_build_extra_context(self):
        view = JobApplicationNoteCreateView()
        extra = view.build_extra_context()
        assert getattr(extra, "app_kind", None) == "job application note"
        assert "Create Job Application Note" in getattr(extra, "page_title", "")


class TestJobApplicationNoteDetailView:

    @patch("apps.applications.views.JobApplicationNoteSelector.get")
    def test_get_object_calls_selector(
            self, mock_get, job_application1, app_note1
    ):
        mock_get.return_value = app_note1

        request = RequestFactory().get("/")
        request.user = job_application1.owner

        view = JobApplicationNoteDetailView()
        view.request = request
        view.kwargs = {"pk": app_note1.pk}

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=job_application1.owner, obj_id=app_note1.pk
        )
        assert result is app_note1

    @patch("apps.applications.views.JobApplicationNoteSelector.get")
    def test_dispatch_translates_selector_get_exceptions_to_404(
            self, mock_get, job_application1
    ):
        mock_get.side_effect = ResourceNotFoundError("missing")

        request = RequestFactory().get("/")
        request.user = job_application1.owner

        view = JobApplicationNoteDetailView()
        view.request = request
        view.kwargs = {"pk": "123"}

        with pytest.raises(Http404):
            view.dispatch(request)

    def test_build_app_context(self, app_note1):
        view = JobApplicationNoteDetailView()
        view.object = app_note1

        ctx = view.build_app_context()
        assert ctx.workspace_id == app_note1.job_application.workspace.workspace_id
        assert ctx.company_id == app_note1.job_application.job_position.company.pk
        assert ctx.position_id == app_note1.job_application.job_position.pk
        assert ctx.application_id == app_note1.job_application.pk
        assert ctx.application_note_id == app_note1.pk


class TestJobApplicationNoteUpdateView:

    @patch("apps.applications.views.JobApplicationNoteSelector.get")
    def test_get_object_calls_selector(self, mock_get, app_note1):
        mock_get.return_value = app_note1

        request = RequestFactory().get("/")
        request.user = app_note1.job_application.workspace.owner

        view = JobApplicationNoteUpdateView()
        view.request = request
        view.kwargs = {"pk": app_note1.pk}

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=app_note1.job_application.workspace.owner, obj_id=app_note1.pk
        )
        assert result is app_note1

    @patch("apps.applications.views.redirect")
    @patch("apps.applications.views.JobApplicationNoteService.update")
    def test_form_valid_calls_service(self, mock_update, mock_redirect, app_note1):
        mock_redirect.return_value = HttpResponse()

        form = Mock()
        form.cleaned_data = {"title": "Edited", "content": "Changed"}

        request = RequestFactory().post("/")
        request.user = app_note1.job_application.workspace.owner

        view = JobApplicationNoteUpdateView()
        view.request = request
        view.object = app_note1
        view.kwargs = {"pk": app_note1.pk}

        result = view.form_valid(form)

        mock_update.assert_called_once()
        kwargs = mock_update.call_args.kwargs

        assert kwargs["user"] == app_note1.job_application.workspace.owner
        assert kwargs["validated_data"] == form.cleaned_data
        assert (kwargs["context"].workspace_id ==
                app_note1.job_application.workspace.workspace_id)

        assert (kwargs["context"].company_id ==
                app_note1.job_application.job_position.company.pk)

        assert (kwargs["context"].job_position_id ==
                app_note1.job_application.job_position.pk)

        assert kwargs["context"].job_application_id == app_note1.job_application.pk
        assert kwargs["context"].id == app_note1.pk

        mock_redirect.assert_called_once()
        assert result is mock_redirect.return_value

    def test_get_success_url(self, app_note1):
        view = JobApplicationNoteUpdateView()
        view.object = app_note1

        url = view.get_success_url()
        assert f"applications/{app_note1.job_application.pk}/" in url

    def test_build_extra_context(self):
        view = JobApplicationNoteUpdateView()
        extra = view.build_extra_context()
        assert getattr(extra, "app_kind", None) == "job application note"
        assert "Update Job Application Note" in getattr(extra, "page_title", "")


class TestJobApplicationNoteDeleteView:

    @patch("apps.applications.views.JobApplicationNoteSelector.get")
    def test_get_object_calls_selector(self, mock_get, app_note1):
        mock_get.return_value = app_note1

        request = RequestFactory().get("/")
        request.user = app_note1.job_application.workspace.owner

        view = JobApplicationNoteDeleteView()
        view.request = request
        view.kwargs = {"pk": app_note1.pk}

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=app_note1.job_application.workspace.owner, obj_id=app_note1.pk
        )
        assert result is app_note1

    @patch("apps.applications.views.redirect")
    @patch("apps.applications.views.JobApplicationNoteService.remove")
    @patch("apps.applications.views.JobApplicationNoteSelector.get")
    def test_post_calls_remove_service(
            self, mock_get, mock_remove, mock_redirect, app_note1
    ):
        mock_get.return_value = app_note1
        mock_redirect.return_value = HttpResponse()

        request = RequestFactory().post("/")
        request.user = app_note1.job_application.workspace.owner

        view = JobApplicationNoteDeleteView()
        view.request = request
        view.kwargs = {"pk": str(app_note1.pk)}

        result = view.post(request, pk=str(app_note1.pk))

        mock_remove.assert_called_once()
        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == app_note1.job_application.workspace.owner
        ctx = kwargs["context"]
        assert ctx.workspace_id == app_note1.job_application.workspace.workspace_id
        assert ctx.company_id == app_note1.job_application.job_position.company.pk
        assert ctx.job_position_id == app_note1.job_application.job_position.pk
        assert ctx.job_application_id == app_note1.job_application.pk

        mock_redirect.assert_called_once()
        assert result is mock_redirect.return_value
