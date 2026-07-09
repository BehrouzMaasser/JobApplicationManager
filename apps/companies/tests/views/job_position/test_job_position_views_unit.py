import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory

from apps.companies.views import (
    JobPositionListView,
    JobPositionCreateView,
    JobPositionDetailView,
    JobPositionUpdateView,
    JobPositionDeleteView,
)

from apps.companies.services.contexts.company_context import CompanyChildContext

pytestmark = pytest.mark.django_db


class TestJobPositionListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.JobPositionSelector.list")
    def test_get_queryset_calls_selector(
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
        assert (kwargs["filters"].company_id ==
                str(job_position1_user1.company.pk))

        assert result is queryset

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        user1,
        co1_ws1_user1,
    ):
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

        assert context.workspace_id == co1_ws1_user1.workspace.workspace_id
        assert context.company_id == co1_ws1_user1.pk


class TestJobPositionCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.JobPositionService.create")
    def test_form_valid_calls_service(
        self,
        mock_create,
        mock_redirect,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "T1",
            "description": "description",
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

        mock_create.assert_called_once()

        kwargs = mock_create.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert isinstance(kwargs["context"], CompanyChildContext)
        assert kwargs["context"].workspace_id == co1_ws1_user1.workspace.workspace_id
        assert kwargs["context"].company_id == co1_ws1_user1.pk
        assert kwargs["context"].id is None

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(self, co1_ws1_user1):

        view = JobPositionCreateView()
        view.kwargs = {
            "company_id": co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(self, co1_ws1_user1):

        view = JobPositionCreateView()
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        context = view.build_app_context()

        assert context.workspace_id == co1_ws1_user1.workspace.workspace_id
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
            job_position_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
            self,
            job_position1_user1,
    ):
        request = RequestFactory().get("/")

        view = JobPositionDetailView()
        view.request = request
        view.object = job_position1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert context.company_id == job_position1_user1.company.pk
        assert context.position_id == job_position1_user1.pk

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
            job_position_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.JobPositionService.update")
    def test_form_valid_calls_service(
        self,
        mock_update,
        mock_redirect,
        user1,
        job_position1_user1,
    ):
        response = HttpResponse()
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

        mock_update.assert_called_once()

        kwargs = mock_update.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert kwargs["context"].workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert kwargs["context"].company_id == job_position1_user1.company.pk
        assert kwargs["context"].id == job_position1_user1.pk

        mock_redirect.assert_called_once()

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

        assert context.company_id == job_position1_user1.company.pk
        assert context.position_id == job_position1_user1.pk

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
            job_position_id=job_position1_user1.pk,
        )

        assert result is job_position1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.JobPositionService.remove")
    @patch("apps.companies.views.JobPositionSelector.get")
    def test_post_calls_remove_service(
        self,
        mock_get,
        mock_remove,
        mock_redirect,
        user1,
        job_position1_user1,
    ):
        response = HttpResponse()

        mock_get.return_value = job_position1_user1
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = JobPositionDeleteView()

        view.request = request
        view.kwargs = {
            "pk": job_position1_user1.pk,
        }

        result = view.post(
            request,
            pk=job_position1_user1.pk,
        )

        mock_remove.assert_called_once()

        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == user1

        assert kwargs["context"].workspace_id == (
            job_position1_user1.company.workspace.workspace_id
        )

        assert kwargs["context"].company_id == job_position1_user1.company.pk
        assert kwargs["context"].id == job_position1_user1.pk

        mock_redirect.assert_called_once()

        assert result is response

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

        assert context.company_id == job_position1_user1.company.pk
        assert context.position_id == job_position1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = JobPositionDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "job position"
        assert context.page_title == "Delete Job Position"
