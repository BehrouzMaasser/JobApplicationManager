# apps/core/mixins/view_exception_handler.py

import logging

from django.http import Http404, HttpResponseBadRequest, HttpResponseServerError

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    DomainInvariantViolationError,
    InfrastructureViolationError,
)

logger = logging.getLogger(__name__)


class ViewExceptionHandlerMixin:

    def dispatch(self, request, *args, **kwargs):

        try:
            return super().dispatch(request, *args, **kwargs)

        except ResourceNotFoundError as exc:
            raise Http404(exc.message)

        except DomainInvariantViolationError as exc:
            logger.exception(exc)
            return HttpResponseBadRequest(
                content="The submitted data could not be processed."
            )

        except InfrastructureViolationError as exc:
            logger.exception(exc)
            return HttpResponseServerError(
                content="An unexpected error occurred, contact admin."
            )
