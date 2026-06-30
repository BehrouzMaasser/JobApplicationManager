import uuid
from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from apps.core.contexts.app_context import AppContext

from apps.core.contexts.extra_context import ExtraContext

from apps.workspaces.views import (
    WorkspaceCreateView,
    WorkspaceDeleteView,
    WorkspaceDetailView,
    WorkspaceListView,
    WorkspaceUpdateView,
)


class TestWorkspaceListView:

    @patch("apps.workspaces.views.WorkspaceSelector.list")
    def test_get_queryset_calls_selector(self, mock_list, user1):

        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)

        assert result is queryset


class TestWorkspaceCreateView:

    @patch("apps.workspaces.views.redirect")
    @patch("apps.workspaces.views.WorkspaceService.create")
    def test_form_valid_calls_service_and_redirects(
        self,
        mock_create,
        mock_redirect,
        user1,
    ):

        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "Backend Workspace"
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceCreateView()
        view.request = request
        view.success_url = "/success/"

        result = view.form_valid(form)

        mock_create.assert_called_once_with(
            user=user1,
            validated_data=form.cleaned_data,
        )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    def test_build_extra_context(self):

        view = WorkspaceCreateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Create Workspace"


class TestWorkspaceDetailView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceDetailView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            workspace_id="workspace-id",
        )

        assert result is workspace

    @patch("apps.workspaces.views.company_list_url")
    def test_build_app_context(
        self,
        mock_company_list_url,
    ):

        mock_company_list_url.return_value = "/companies/"

        view = WorkspaceDetailView()
        view.kwargs = {
            "workspace_id": "workspace-id"
        }

        context = view.build_app_context()

        mock_company_list_url.assert_called_once_with(
            workspace_id="workspace-id"
        )

        assert isinstance(context, AppContext)
        assert context.companies_list_url == "/companies/"


class TestWorkspaceUpdateView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            workspace_id="workspace-id",
        )

        assert result is workspace

    @patch("apps.workspaces.views.redirect")
    @patch("apps.workspaces.views.WorkspaceService.update")
    def test_form_valid_calls_service_and_redirects(
        self,
        mock_update,
        mock_redirect,
        user1,
    ):

        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "Updated Workspace"
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id"
        }

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ) as mock_success_url:

            result = view.form_valid(form)

        mock_update.assert_called_once_with(
            user=user1,
            workspace_id="workspace-id",
            validated_data=form.cleaned_data,
        )

        mock_success_url.assert_called_once()

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    def test_get_success_url(self):

        view = WorkspaceUpdateView()

        some_workspace_id = uuid.uuid4()

        view.kwargs = {
            "workspace_id": some_workspace_id
        }

        assert (
            view.get_success_url() == reverse(
                "workspace-detail-web",
                kwargs={"workspace_id": some_workspace_id}
            )
        )

    def test_build_extra_context(self):

        view = WorkspaceUpdateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Update Workspace"


class TestWorkspaceDeleteView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceDeleteView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            workspace_id="workspace-id",
        )

        assert result is workspace

    @patch("apps.workspaces.views.redirect")
    @patch("apps.workspaces.views.WorkspaceService.remove")
    def test_post_calls_service_and_redirects(
        self,
        mock_remove,
        mock_redirect,
        user1,
    ):

        response = HttpResponse()
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceDeleteView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id"
        }
        view.success_url = "/success/"

        result = view.post(request)

        mock_remove.assert_called_once_with(
            user=user1,
            workspace_id="workspace-id",
        )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    def test_build_extra_context(self):

        view = WorkspaceDeleteView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Delete Workspace"
