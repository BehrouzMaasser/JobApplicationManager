from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from apps.core.contexts.extra_context import ExtraContext

from apps.documents.views import (
    DocumentCreateView,
    DocumentDeleteView,
    DocumentDetailView,
    DocumentListView,
    DocumentUpdateView,
)


class TestDocumentListView:

    @patch("apps.documents.views.DocumentSelector.list")
    def test_get_queryset_calls_selector(self, mock_list, user1):

        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)

        assert result is queryset


class TestDocumentCreateView:

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentService.create")
    def test_form_valid_calls_service_and_redirects(
        self,
        mock_create,
        mock_redirect,
        document_type_user1,
        fake_file1
    ):

        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "T1",
            "document_type": document_type_user1.pk,
            "file": fake_file1,
        }

        request = RequestFactory().post("/")
        request.user = document_type_user1.owner

        view = DocumentCreateView()
        view.request = request

        result = view.form_valid(form)

        mock_create.assert_called_once_with(
            user=document_type_user1.owner,
            validated_data=form.cleaned_data,
        )

        mock_redirect.assert_called_once_with(reverse("document-list-web"))

        assert result is response

    def test_build_extra_context(self):

        view = DocumentCreateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document"
        assert context.page_title == "Create Document"


class TestDocumentDetailView:

    @patch("apps.documents.views.DocumentSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentDetailView()
        view.request = request
        view.kwargs = {
            "pk": "Document-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_id="Document-id",
        )

        assert result is queryset


class TestDocumentUpdateView:

    @patch("apps.documents.views.DocumentSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentUpdateView()
        view.request = request
        view.kwargs = {
            "pk": "Document-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_id="Document-id",
        )

        assert result is queryset

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentService.update")
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
            "name": "Updated Document"
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentUpdateView()
        view.request = request
        view.kwargs = {
            "pk": "Document-id"
        }

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ) as mock_success_url:

            result = view.form_valid(form)

        mock_update.assert_called_once_with(
            user=user1,
            document_id="Document-id",
            validated_data=form.cleaned_data,
        )

        mock_success_url.assert_called_once()

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    def test_get_success_url(self):

        view = DocumentUpdateView()

        some_document_id = 99999

        view.kwargs = {
            "pk": some_document_id
        }

        assert (
            view.get_success_url() == reverse(
                "document-detail-web",
                kwargs={"pk": some_document_id}
            )
        )

    def test_build_extra_context(self):

        view = DocumentUpdateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document"
        assert context.page_title == "Update Document"


class TestDocumentDeleteView:

    @patch("apps.documents.views.DocumentSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentDeleteView()
        view.request = request
        view.kwargs = {
            "pk": "Document-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_id="Document-id",
        )

        assert result is queryset

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentService.remove")
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

        view = DocumentDeleteView()
        view.request = request
        view.kwargs = {
            "pk": "999999"
        }

        result = view.post(request)

        mock_remove.assert_called_once_with(
            user=user1,
            document_id="999999",
        )

        mock_redirect.assert_called_once_with(
            reverse("document-list-web")
        )

        assert result is response

    def test_build_extra_context(self):

        view = DocumentDeleteView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document"
        assert context.page_title == "Delete Document"
