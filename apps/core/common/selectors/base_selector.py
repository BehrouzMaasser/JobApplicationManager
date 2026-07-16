from abc import ABC
from typing import Generic, TypeVar

from django.db.models import Model
from django.db.models import QuerySet

from apps.accounts.models import User

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    InfrastructureViolationError
)

DjangoModel = TypeVar("DjangoModel", bound=Model)


class BaseSelector(ABC, Generic[DjangoModel]):
    """
    Base class for read-only selectors.

    A selector encapsulates database retrieval logic for a single domain model,
    including resource lookup, ownership-based access control, query filtering,
    and exception translation.

    Subclasses are expected to define the target model and implement any
    domain-specific filtering by overriding ``apply_filters()`` when needed.
    """

    MODEL: type[DjangoModel] | None = None
    RESOURCE_NAME: str | None = None
    OWNER_PATH: str | None = None
    LOOKUP_FIELD: str | None = None

    def __init_subclass__(cls):
        super().__init_subclass__()

        if cls is BaseSelector:
            return

        if cls.MODEL is None:
            raise TypeError(f"{cls.__name__} must define MODEL")

        if cls.RESOURCE_NAME is None:
            raise TypeError(f"{cls.__name__} must define RESOURCE_NAME")

        if cls.LOOKUP_FIELD is None:
            raise TypeError(f"{cls.__name__} must define LOOKUP_FIELD")

    @classmethod
    def base_queryset(cls) -> QuerySet[DjangoModel]:
        """
        Return the base queryset for the selector's model.

        Subclasses may override this method to customize the default queryset,
        for example by applying ``select_related()``, ``prefetch_related()``,
        annotations, or default ordering.
        """

        return cls.MODEL.objects.all()

    @classmethod
    def accessible_queryset(cls, *, user) -> QuerySet[DjangoModel]:
        """
        Return the subset of the base queryset accessible to the given user.

        When ``OWNER_PATH`` is defined, ownership filtering is applied using the
        configured relationship path. Otherwise, an empty queryset is returned,
        requiring subclasses to explicitly opt into unrestricted access if
        appropriate.
        """

        queryset = cls.base_queryset()

        if cls.OWNER_PATH:
            return queryset.filter(
                **{cls.OWNER_PATH.replace(".", "__"): user}
            )
        return queryset.none()

    @classmethod
    def get(cls, *, user: User, obj_id) -> DjangoModel:
        """
        Retrieve a single accessible resource by its lookup field.

        Raises:
            ResourceNotFoundError:
                If no accessible resource matches the given identifier.

            InfraStructureViolationError:
                If an unexpected database error occurs during retrieval.
        """

        try:
            return cls.accessible_queryset(user=user).get(
                **{cls.LOOKUP_FIELD: obj_id}
            )
        except cls.MODEL.DoesNotExist:
            raise ResourceNotFoundError(f"{cls.RESOURCE_NAME} {obj_id} not found")
        except Exception as e:
            raise InfrastructureViolationError(
                f"Failed retrieving {cls.RESOURCE_NAME} {obj_id}."
            ) from e

    @classmethod
    def list(cls, *, user, filters=None) -> QuerySet[DjangoModel]:
        """
        Return the queryset of resources accessible to the given user.

        If filter criteria are provided, they are applied using
        ``apply_filters()`` before returning the queryset.
        """

        queryset = cls.accessible_queryset(user=user)

        if filters is None:
            return queryset

        return cls.apply_filters(queryset, filters)

    @classmethod
    def apply_filters(
            cls, queryset: QuerySet[DjangoModel], filters
    ) -> QuerySet[DjangoModel]:
        """
        Apply selector-specific filters to the queryset.

        Subclasses should override this method to implement domain-specific
        filtering while preserving the ownership restrictions applied by
        ``accessible_queryset()``.

        The default implementation returns the queryset unchanged.
        """

        return queryset
