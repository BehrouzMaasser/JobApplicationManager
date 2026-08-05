import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory

from apps.companies.views import (
    CompanyNoteListView,
    CompanyNoteCreateView,
    CompanyNoteDetailView, CompanyNoteDeleteView, CompanyNoteUpdateView,
)

pytestmark = pytest.mark.django_db


class TestCompanyNoteListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.CompanyNoteSelector.list")
    def test_get_queryset_calls_selector(
        self,
        mock_list,
        user1,
        co_note1_co1_ws1_user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "company_id": co_note1_co1_ws1_user1.company.pk,
            },
        )
        request.user = user1

        view = CompanyNoteListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert (
            kwargs["filters"].company_id
            == str(co_note1_co1_ws1_user1.company.pk)
        )

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

        view = CompanyNoteListView()
        view.request = request

        context = view.build_app_context()

        assert context.workspace_id == co1_ws1_user1.workspace.workspace_id
        assert context.company_id == co1_ws1_user1.pk


class TestCompanyNoteCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.CompanyNoteCreateView.execute_service")
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
            "title": "Title",
            "content": "Content",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyNoteCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        kwargs = mock_execute_service.call_args.kwargs

        assert kwargs["form"] is form
        assert callable(kwargs["operation"])

        mock_redirect.assert_called_once_with(view.get_success_url())

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co1_ws1_user1,
    ):
        view = CompanyNoteCreateView()

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
        view = CompanyNoteCreateView()

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
        view = CompanyNoteCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "company note"
        assert context.page_title == "Create Company Note"


class TestCompanyNoteDetailView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyNoteSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_note1_co1_ws1_user1,
    ):
        mock_get.return_value = co_note1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyNoteDetailView()
        view.request = request
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co_note1_co1_ws1_user1.pk,
        )

        assert result is co_note1_co1_ws1_user1

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co_note1_co1_ws1_user1,
    ):
        view = CompanyNoteDetailView()

        view.object = co_note1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co_note1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_note1_co1_ws1_user1.company.pk
        assert context.note_id == co_note1_co1_ws1_user1.pk

        assert context.applications_list_url is None
        assert context.companies_list_url is None
        assert context.positions_list_url is None
        assert context.company_emails_list_url is None
        assert context.company_notes_list_url is None

class TestCompanyNoteUpdateView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyNoteSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_note1_co1_ws1_user1,
    ):
        mock_get.return_value = co_note1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyNoteUpdateView()
        view.request = request
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co_note1_co1_ws1_user1.pk,
        )

        assert result is co_note1_co1_ws1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.CompanyNoteUpdateView.execute_service")
    @patch("apps.companies.views.redirect")
    def test_form_valid_executes_service_and_redirects(
        self,
        mock_redirect,
        mock_execute_service,
        user1,
        co_note1_co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_execute_service.return_value = None
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "Updated",
            "content": "Updated content",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyNoteUpdateView()
        view.request = request
        view.object = co_note1_co1_ws1_user1
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        kwargs = mock_execute_service.call_args.kwargs

        assert kwargs["form"] is form
        assert callable(kwargs["operation"])

        mock_redirect.assert_called_once_with(view.get_success_url())

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co_note1_co1_ws1_user1,
    ):
        view = CompanyNoteUpdateView()

        view.object = co_note1_co1_ws1_user1
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co_note1_co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co_note1_co1_ws1_user1,
    ):
        view = CompanyNoteUpdateView()

        view.object = co_note1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co_note1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_note1_co1_ws1_user1.company.pk
        assert context.note_id == co_note1_co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):
        view = CompanyNoteUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "company note"
        assert context.page_title == "Update Company Note"


class TestCompanyNoteDeleteView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyNoteSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_note1_co1_ws1_user1,
    ):
        mock_get.return_value = co_note1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyNoteDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co_note1_co1_ws1_user1.pk,
        )

        assert result is co_note1_co1_ws1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.CompanyNoteService.remove")
    @patch("apps.companies.views.redirect")
    def test_post_executes_remove_service_and_redirects(
        self,
        mock_redirect,
        mock_remove,
        user1,
        co_note1_co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyNoteDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co_note1_co1_ws1_user1.pk,
        }

        result = view.post(
            request,
            pk=co_note1_co1_ws1_user1.pk,
        )

        mock_remove.assert_called_once()

        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == user1

        context = kwargs["context"]

        assert (
            context.workspace_id
            == co_note1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_note1_co1_ws1_user1.company.pk
        assert context.id == co_note1_co1_ws1_user1.pk

        mock_redirect.assert_called_once_with(
            view.get_success_url()
        )

        assert result is response

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co_note1_co1_ws1_user1,
    ):
        view = CompanyNoteDeleteView()

        view.object = co_note1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co_note1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_note1_co1_ws1_user1.company.pk
        assert context.note_id == co_note1_co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):
        view = CompanyNoteDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "company note"
        assert context.page_title == "Delete Company Note"
