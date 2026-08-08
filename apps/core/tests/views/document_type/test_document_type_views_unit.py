from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory
from django.urls import reverse

from apps.core.contexts.extra_context import ExtraContext
from apps.core.exceptions.exceptions import BusinessRuleViolationError

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

        # Don't assert exact kwarg names — verify essential behaviour.
        mock_create.assert_called_once()
        _, kwargs = mock_create.call_args
        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data
        assert "context" in kwargs

        mock_redirect.assert_called_once_with(reverse("document-type-list-web"))

        assert result is response

    def test_build_extra_context(self):

        view = DocumentTypeCreateView()

        context = view.build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "document type"
        assert context.page_title == "Create Document Type"

    @patch("apps.documents.views.ServiceFormErrorMixin.add_service_errors_to_form")
    @patch("apps.documents.views.DocumentTypeService.create")
    def test_form_valid_handles_service_validation_error(
        self,
        mock_create,
        mock_add_errors,
        user1,
    ):
        """
        When the service raises a BusinessRuleViolationError the mixin should
        add errors to the form instead of letting the exception bubble.
        """
        # Simulate service validation failure
        mock_create.side_effect = BusinessRuleViolationError(
            fields=["name"],
            messages=["Invalid name"]
        )

        form = Mock()
        # Provide an add_error so that code paths using form.add_error won't break
        form.add_error = Mock()
        request = RequestFactory().post("/")
        request.user = user1

        view = DocumentTypeCreateView()
        view.request = request

        # Call form_valid which uses execute_service internally
        view.form_valid(form)

        # Mixin's add_service_errors_to_form should be invoked
        mock_add_errors.assert_called_once()


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

        # Verify selector was called and crucial kwargs are present
        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        assert kwargs["user"] == user1
        assert kwargs.get("obj_id") == "DocumentType-id"

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

        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        assert kwargs["user"] == user1
        assert kwargs.get("obj_id") == "DocumentType-id"

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

        mock_update.assert_called_once()
        _, kwargs = mock_update.call_args
        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data
        # Service should receive a context object identifying the target
        assert "context" in kwargs
        assert getattr(kwargs["context"], "id", None) == view.kwargs["pk"]

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

        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        assert kwargs["user"] == user1
        assert kwargs.get("obj_id") == "DocumentType-id"

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

        mock_remove.assert_called_once()
        _, kwargs = mock_remove.call_args
        assert kwargs["user"] == user1
        assert "context" in kwargs
        assert getattr(kwargs["context"], "id", None) == view.kwargs["pk"]

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
