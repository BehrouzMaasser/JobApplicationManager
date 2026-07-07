import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory

from apps.companies.views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
)

from apps.companies.services.contexts.company_context import CompanyContext

pytestmark = pytest.mark.django_db


class TestCompanyListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.CompanySelector.list")
    def test_get_queryset_calls_selector(
        self,
        mock_list,
        user1,
        workspace1_user1,
    ):
        queryset = Mock()

        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": workspace1_user1.workspace_id,
            },
        )
        request.user = user1

        view = CompanyListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["filters"].workspace_id == str(workspace1_user1.workspace_id)

        assert result is queryset

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        user1,
        workspace1_user1,
    ):
        request = RequestFactory().get(
            "/",
            {
                "workspace_id": workspace1_user1.workspace_id,
            },
        )
        request.user = user1

        view = CompanyListView()
        view.request = request

        context = view.build_app_context()

        assert context.workspace_id == str(workspace1_user1.workspace_id)


class TestCompanyCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyService.create")
    def test_form_valid_calls_service(
        self,
        mock_create,
        mock_redirect,
        user1,
        workspace1_user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "ACME",
            "website": "https://acme.com",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        result = view.form_valid(form)

        mock_create.assert_called_once()

        kwargs = mock_create.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert isinstance(kwargs["context"], CompanyContext)
        assert kwargs["context"].workspace_id == workspace1_user1.workspace_id
        assert kwargs["context"].id is None

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(self, workspace1_user1):

        view = CompanyCreateView()
        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        url = view.get_success_url()

        assert str(workspace1_user1.workspace_id) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(self, workspace1_user1):

        view = CompanyCreateView()
        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        context = view.build_app_context()

        assert context.workspace_id == workspace1_user1.workspace_id

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Create Company"


class TestCompanyDetailView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
            self,
            mock_get,
            user1,
            co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyDetailView()
        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
            self,
            co1_ws1_user1,
    ):
        request = RequestFactory().get("/")

        view = CompanyDetailView()
        view.request = request
        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )

        assert context.company_id == co1_ws1_user1.pk

        assert context.applications_list_url is not None
        assert context.companies_list_url is not None
        assert context.positions_list_url is not None
        assert context.company_emails_list_url is not None
        assert context.company_notes_list_url is not None


class TestCompanyUpdateView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyUpdateView()
        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyService.update")
    def test_form_valid_calls_service(
        self,
        mock_update,
        mock_redirect,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "Updated Company",
            "website": "https://updated.com",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyUpdateView()
        view.request = request
        view.object = co1_ws1_user1
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_update.assert_called_once()

        kwargs = mock_update.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert kwargs["context"].workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )

        assert kwargs["context"].id == co1_ws1_user1.pk

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co1_ws1_user1,
    ):
        view = CompanyUpdateView()

        view.kwargs = {
            "pk": co1_ws1_user1.pk,
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
        view = CompanyUpdateView()
        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )

        assert context.company_id == co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Update Company"


class TestCompanyDeleteView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyService.remove")
    @patch("apps.companies.views.CompanySelector.get")
    def test_post_calls_remove_service(
        self,
        mock_get,
        mock_remove,
        mock_redirect,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_get.return_value = co1_ws1_user1
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.post(
            request,
            pk=co1_ws1_user1.pk,
        )

        mock_remove.assert_called_once()

        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == user1

        assert kwargs["context"].workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )

        assert kwargs["context"].id == co1_ws1_user1.pk

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        view = CompanyDeleteView()
        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co1_ws1_user1.workspace.workspace_id
        )

        assert context.company_id == co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Delete Company"
