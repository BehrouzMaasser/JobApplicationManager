from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from apps.core.contexts.extra_context import ExtraContext

from apps.documents.views import (
    DocumentTypeCreateView,
    DocumentTypeDeleteView,
    DocumentTypeDetailView,
    DocumentTypeListView,
    DocumentTypeUpdateView,
)


class TestDocumentTypeListView:

    @patch("apps.documents.views.DocumentTypeSelector.list")
    def test_get_queryset_calls_selector(self, mock_list, user1):

        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentTypeListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)

        assert result is queryset


class TestDocumentTypeCreateView:

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentTypeService.create")
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
            "name": "T1"
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentTypeCreateView()
        view.request = request

        result = view.form_valid(form)

        mock_create.assert_called_once_with(
            user=user1,
            validated_data=form.cleaned_data,
        )

        mock_redirect.assert_called_once_with(reverse("document-type-list-web"))

        assert result is response

    def test_build_extra_context(self):

        view = DocumentTypeCreateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document type"
        assert context.page_title == "Create Document Type"


class TestDocumentTypeDetailView:

    @patch("apps.documents.views.DocumentTypeSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentTypeDetailView()
        view.request = request
        view.kwargs = {
            "pk": "DocumentType-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_type_id="DocumentType-id",
        )

        assert result is queryset


class TestDocumentTypeUpdateView:

    @patch("apps.documents.views.DocumentTypeSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = DocumentTypeUpdateView()
        view.request = request
        view.kwargs = {
            "pk": "DocumentType-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_type_id="DocumentType-id",
        )

        assert result is queryset

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentTypeService.update")
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
            "name": "Updated DocumentType"
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentTypeUpdateView()
        view.request = request
        view.kwargs = {
            "pk": "DocumentType-id"
        }

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ) as mock_success_url:

            result = view.form_valid(form)

        mock_update.assert_called_once_with(
            user=user1,
            document_type_id="DocumentType-id",
            validated_data=form.cleaned_data,
        )

        mock_success_url.assert_called_once()

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    def test_get_success_url(self):

        view = DocumentTypeUpdateView()

        some_document_type_id = 99999

        view.kwargs = {
            "pk": some_document_type_id
        }

        assert (
            view.get_success_url() == reverse(
                "document-type-detail-web",
                kwargs={"pk": some_document_type_id}
            )
        )

    def test_build_extra_context(self):

        view = DocumentTypeUpdateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document type"
        assert context.page_title == "Update Document Type"


class TestDocumentTypeDeleteView:

    @patch("apps.documents.views.DocumentTypeSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
    ):

        queryset = Mock()
        mock_get.return_value = queryset

        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentTypeDeleteView()
        view.request = request
        view.kwargs = {
            "pk": "DocumentType-id"
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            document_type_id="DocumentType-id",
        )

        assert result is queryset

    @patch("apps.documents.views.redirect")
    @patch("apps.documents.views.DocumentTypeService.remove")
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

        view = DocumentTypeDeleteView()
        view.request = request
        view.kwargs = {
            "pk": "999999"
        }

        result = view.post(request)

        mock_remove.assert_called_once_with(
            user=user1,
            document_type_id="999999",
        )

        mock_redirect.assert_called_once_with(
            reverse("document-type-list-web")
        )

        assert result is response

    def test_build_extra_context(self):

        view = DocumentTypeDeleteView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document type"
        assert context.page_title == "Delete Document Type"
