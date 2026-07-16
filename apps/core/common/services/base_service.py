"""
Base class for write services.

Services coordinate business use-cases, enforce business rules,
validate models, and persist changes.

Subclasses should only implement domain-specific behavior while
delegating common persistence logic to this base class.
"""

from abc import ABC, abstractmethod
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.core.common.contexts.base_context import BaseContext
from apps.core.common.selectors.base_selector import BaseSelector

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError, AppError, InfrastructureViolationError
)


class BaseService(ABC):

    _REQUIRED_CONFIG = (
        "MODEL",
        "SELECTOR",
        "CREATE_FIELDS",
        "SCALAR_UPDATABLE_FIELDS",
        "M2M_UPDATABLE_FIELDS",
        "REQUIRED_M2M_FIELDS",
        "NON_EMPTY_M2M_FIELDS",
        "M2M_OWNER_FIELD_MAP",
    )

    #
    # Service configuration
    #

    MODEL: type[models.Model] = None
    SELECTOR: type[BaseSelector] = None

    CREATE_FIELDS: tuple[str, ...] = None
    SCALAR_UPDATABLE_FIELDS: tuple[str, ...] = None
    M2M_UPDATABLE_FIELDS: tuple[str, ...] = None
    REQUIRED_M2M_FIELDS: tuple[str, ...] = None
    NON_EMPTY_M2M_FIELDS: tuple[str, ...] = None
    M2M_OWNER_FIELD_MAP: dict[str, str] = None

    def __init_subclass__(cls):

        super().__init_subclass__()

        cls._validate_configuration()

    #
    # Public API
    #

    @classmethod
    @transaction.atomic
    def create(
            cls, user: User, context: BaseContext, validated_data: dict[str, Any]
    ) -> models.Model:
        """Create and persist a new model instance."""

        try:

            model_data = {**validated_data}

            create_dependencies = cls._resolve_create_dependencies(
                user,
                context
            )

            if create_dependencies and isinstance(create_dependencies, dict):
                model_data = {**model_data, **create_dependencies}

            instance = cls._build_model(**model_data)

            cls._create_validate(
                user=user,
                instance=instance,
                validated_data=validated_data
            )

            cls._pre_save(user=user, validated_data=validated_data)

            cls._save(instance)

            cls._create_post_save(instance, validated_data)

            return instance

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while creating {cls.MODEL.__name__}."
            ) from exc

    @classmethod
    @transaction.atomic
    def update(
            cls,
            user: User,
            context: BaseContext,
            validated_data: dict[str, Any]
    ) -> models.Model:
        """Update and persist an existing model instance."""

        try:
            instance = cls._resolve_instance(user=user, context=context)

            cls._update_validate(
                user=user,
                instance=instance,
                validated_data=validated_data
            )

            cls._pre_save(user=user, validated_data=validated_data)

            cls._apply_scalar_updates(
                instance=instance,
                validated_data=validated_data
            )

            cls._save(instance)

            cls._update_post_save(instance, validated_data)

            return instance

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while updating {cls.MODEL.__name__}."
            ) from exc

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: BaseContext
    ) -> dict[str, Any]:
        """
        Resolve additional model fields required during creation.

        Returns a mapping whose keys are model field names and whose values
        will be merged into the data passed to `_build_model()`.

        The default implementation returns an empty dictionary.
        """

        return {}

    @classmethod
    def _pre_save(cls, *, user: User, validated_data: dict[str, Any]) -> None:

        cls._validate_m2m_ownership(user=user, validated_data=validated_data)
        cls._validate_required_m2m_fields(validated_data=validated_data)

    @classmethod
    def _create_post_save(
            cls,
            instance: models.Model,
            validated_data: dict[str, Any]
    ) -> None:
        """
        Execute common post-save operations for updated instances.

        `instance` has already been updated, validated and persisted.

        This hook is responsible for synchronizing many-to-many
        relationships and validating post-save business rules.
        """

        cls._add_m2m_fields(instance=instance, validated_data=validated_data)
        cls._m2m_non_empty_validation(instance)

    @classmethod
    def _update_post_save(
            cls,
            instance: models.Model,
            validated_data: dict[str, Any]
    ) -> None:
        """
        Execute common post-save operations for newly created instances.

        `instance` has already been validated and persisted to the database.

        This hook is responsible for applying many-to-many relationships and
        validating post-save business rules.
        """

        cls._apply_m2m_updates(instance=instance, validated_data=validated_data)
        cls._m2m_non_empty_validation(instance)

    @classmethod
    def _create_validate(
            cls,
            *,
            user: User,
            instance: models.Model,
            validated_data: dict[str, Any]
    ) -> None:
        """
        Execute business validations specific to the create operation.

        `instance` is a newly constructed model instance that has **not**
        been validated or persisted yet.

        This hook should validate business rules without mutating the model.
        """

        pass

    @classmethod
    def _update_validate(
            cls,
            *,
            user: User,
            instance: models.Model,
            validated_data: dict[str, Any]
    ) -> None:
        """
        Execute business validations specific to the update operation.

        `instance` is the current persisted model retrieved from the
        database. Scalar updates have **not** been applied yet.

        This hook should validate whether the requested update is allowed
        before the instance is modified.
        """

        pass

    @classmethod
    @transaction.atomic
    def remove(cls, *, user: User, context: BaseContext) -> None:
        """Delete an existing model instance."""

        try:
            instance = cls._resolve_instance(user=user, context=context)

            instance.delete()

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while removing {cls.MODEL.__name__}."
            ) from exc

    @classmethod
    def _resolve_instance(cls, *, user: User, context: BaseContext) -> models.Model:
        """
        Resolve the aggregate being modified.

        """

        instance = cls.SELECTOR.get(user=user, obj_id=context.id)

        cls._validate_resolved_instance(instance=instance, context=context)

        return instance

    @classmethod
    @abstractmethod
    def _validate_resolved_instance(
            cls,
            *,
            instance: models.Model,
            context: BaseContext
    ) -> None:
        """
        Validate that the resolved aggregate matches the supplied context.

        `instance` is the persisted model returned by the configured
        selector.

        Override this hook to validate parent-child relationships or other
        aggregate invariants.
        """
        ...

    #
    # Validation helpers
    #

    @classmethod
    def _m2m_non_empty_validation(cls, instance: models.Model) -> None:
        """
        Validate that configured many-to-many fields are not empty.

        `instance` must already be persisted because many-to-many relations
        are queried through the database.

        Raises:
            BusinessRuleViolationError:
                If any configured relation is empty.
        """

        empty_required_fields = []

        for field in cls.NON_EMPTY_M2M_FIELDS:
            if not getattr(instance, field).exists():
                empty_required_fields.append(field)

        if empty_required_fields:
            raise BusinessRuleViolationError(
                fields=empty_required_fields,
                messages=["Should not be empty" for _ in empty_required_fields]
            )

    @classmethod
    def _validate_m2m_ownership(
            cls,
            *,
            user: User,
            validated_data: dict[str, Any],
    ) -> None:

        # Make sure the m2m fields are associated to the user
        invalid_fields_with_ids: dict[str, list[str]] = dict()

        for field_name, ownership in cls.M2M_OWNER_FIELD_MAP.items():
            if field_name in validated_data:
                for data in validated_data[field_name]:
                    # Some related models may not expose the configured ownership
                    # attribute.
                    # Those objects are ignored because ownership cannot be
                    # validated for them.
                    try:
                        if getattr(data, ownership) != user:
                            invalid_fields_with_ids.setdefault(
                                field_name, []
                            ).append(data.pk)
                    except AttributeError:
                        continue

        if invalid_fields_with_ids:
            raise DomainInvariantViolationError(
                message="; ".join(
                    f"Current user does not own {field}: {ids}"
                    for field, ids in invalid_fields_with_ids.items()
                )
            )

    @classmethod
    def _validate_required_m2m_fields(
        cls,
        *,
        validated_data: dict[str, Any],
    ) -> None:

        missing = [
            field
            for field in cls.REQUIRED_M2M_FIELDS
            if field not in validated_data
        ]

        if missing:
            raise BusinessRuleViolationError(
                fields=missing,
                messages=["This field is required." for _ in missing]
            )

    #
    # Field helpers
    #

    @classmethod
    def _add_m2m_fields(
            cls,
            *,
            instance: models.Model,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Add many-to-many relations to a newly created instance.

        `instance` must already be persisted because many-to-many relations
        cannot be assigned before the primary key exists.
        """

        for field in cls.M2M_UPDATABLE_FIELDS:
            if field in validated_data:
                getattr(instance, field).add(*validated_data[field])

    @classmethod
    def _apply_m2m_updates(
            cls,
            *,
            instance: models.Model,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Synchronize many-to-many relations of an existing persisted model.

        `instance` must already exist in the database.
        """

        for field in cls.M2M_UPDATABLE_FIELDS:
            if field in validated_data:
                getattr(instance, field).set(validated_data.get(field))

    @classmethod
    def _apply_scalar_updates(
            cls,
            *,
            instance: models.Model,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Apply scalar field updates in memory.

        `instance` is the persisted model retrieved from the database.

        This method only mutates the in-memory object. Validation and
        persistence occur later through `_save()`.
        """

        for field in cls.SCALAR_UPDATABLE_FIELDS:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

    #
    # Persistence helpers
    #

    @classmethod
    def _save(cls, instance: models.Model) -> None:
        """
        Validate and persist the supplied model instance.

        Calls `full_clean()` before saving.

        After this method returns successfully, `instance` is guaranteed to
        be persisted and synchronized with the database.
        """

        instance.full_clean()
        instance.save()

    #
    # Factory helper
    #

    @classmethod
    def _build_model(cls, **kwargs) -> models.Model:

        return cls.MODEL(
            **{
                field: kwargs.get(field)
                for field in cls.CREATE_FIELDS
            }
        )

    @classmethod
    def _validate_configuration(cls):

        if cls is BaseService:
            return

        for attr in cls._REQUIRED_CONFIG:
            if getattr(cls, attr, None) is None:
                raise TypeError(
                    f"{cls.__name__} must define {attr}"
                )

        if not issubclass(cls.MODEL, models.Model):
            raise TypeError(
                f"{cls.__name__}.MODEL must inherit from django.db.models.Model"
            )

        if not issubclass(cls.SELECTOR, BaseSelector):
            raise TypeError(
                f"{cls.__name__}.SELECTOR must inherit from BaseSelector"
            )

        cls._validate_tuple_of_strings(
            "CREATE_FIELDS",
            cls.CREATE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "SCALAR_UPDATABLE_FIELDS",
            cls.SCALAR_UPDATABLE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "M2M_UPDATABLE_FIELDS",
            cls.M2M_UPDATABLE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "REQUIRED_M2M_FIELDS",
            cls.REQUIRED_M2M_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "NON_EMPTY_M2M_FIELDS",
            cls.NON_EMPTY_M2M_FIELDS,
        )

        cls._validate_owner_field_map()

        overlap = (
            set(cls.SCALAR_UPDATABLE_FIELDS)
            & set(cls.M2M_UPDATABLE_FIELDS)
        )

        if overlap:
            raise TypeError(
                "Fields cannot be both scalar and many-to-many: "
                f"{sorted(overlap)}"
            )

        cls._validate_model_fields()

    @classmethod
    def _validate_model_fields(cls) -> None:
        """Validate that all configured field names exist on the model."""

        model_fields = {
            field.name
            for field in cls.MODEL._meta.get_fields() if hasattr(field, "name")
        }

        configured_fields = (
            set(cls.CREATE_FIELDS)
            | set(cls.SCALAR_UPDATABLE_FIELDS)
            | set(cls.M2M_UPDATABLE_FIELDS)
            | set(cls.REQUIRED_M2M_FIELDS)
            | set(cls.NON_EMPTY_M2M_FIELDS)
            | set(cls.M2M_OWNER_FIELD_MAP.keys())
        )

        unknown = configured_fields - model_fields

        if unknown:
            raise TypeError(
                f"{cls.__name__} references unknown model field(s): "
                f"{sorted(unknown)}"
            )

    @classmethod
    def _validate_tuple_of_strings(cls, name: str, value) -> None:
        """Validate that a configuration value is a tuple of unique strings."""

        if not isinstance(value, tuple):
            raise TypeError(f"{name} must be an instance of tuple")

        if len(value) != len(set(value)):
            raise TypeError(f"{name} must not contain duplicate field names")

        for field in value:
            if not isinstance(field, str):
                raise TypeError(
                    f"{name} must contain only field names (str), "
                    f"got {type(field).__name__}"
                )

    @classmethod
    def _validate_owner_field_map(cls) -> None:
        """Validate the M2M_OWNER_FIELD_MAP configuration."""

        value = cls.M2M_OWNER_FIELD_MAP

        if not isinstance(value, dict):
            raise TypeError("M2M_OWNER_FIELD_MAP must be an instance of dict")

        for field, owner in value.items():

            if not isinstance(field, str):
                raise TypeError(
                    "M2M_OWNER_FIELD_MAP keys must be field names (str)"
                )

            if not isinstance(owner, str):
                raise TypeError(
                    "M2M_OWNER_FIELD_MAP values must be attribute paths (str)"
                )
