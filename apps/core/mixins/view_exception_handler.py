# apps/core/mixins/view_exception_handler.py

import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
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

        except (DomainInvariantViolationError, InfrastructureViolationError) as exc:
            logger.exception(exc)
            raise Http404("Something went wrong.")
