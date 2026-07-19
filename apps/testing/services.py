from apps.core.common.services.base_service import BaseService

from .models import DummyItem
from .selectors import DummyItemSelector


class RecordingDummyItemService(BaseService):

    MODEL = DummyItem

    SELECTOR = DummyItemSelector

    CREATE_FIELDS = (
        "owner",
        "name",
    )

    SCALAR_UPDATABLE_FIELDS = (
        "name",
    )

    M2M_UPDATABLE_FIELDS = (
        "tags",
    )

    REQUIRED_M2M_FIELDS = ()

    NON_EMPTY_M2M_FIELDS = ()

    M2M_OWNER_FIELD_MAP = {
        "tags": "owner",
    }

    events = []

    @classmethod
    def clear_events(cls):
        cls.events.clear()

    @classmethod
    def _resolve_create_dependencies(cls, user, context):

        cls.events.append(
            "_resolve_create_dependencies"
        )

        return {
            "owner": user
        }

    @classmethod
    def _create_validate(
            cls,
            *,
            user,
            instance,
            validated_data
    ):

        cls.events.append(
            "_create_validate"
        )

    @classmethod
    def _update_validate(
            cls,
            *,
            user,
            instance,
            validated_data
    ):

        cls.events.append(
            "_update_validate"
        )

    @classmethod
    def _validate_resolved_instance(
            cls,
            *,
            instance,
            context
    ):

        cls.events.append(
            "_validate_resolved_instance"
        )

    @classmethod
    def _pre_save(
            cls,
            *,
            user,
            validated_data
    ):

        cls.events.append(
            "_pre_save"
        )

        super()._pre_save(
            user=user,
            validated_data=validated_data,
        )

    @classmethod
    def _save(cls, instance):

        cls.events.append(
            "_save"
        )

        super()._save(instance)

    @classmethod
    def _create_post_save(
            cls,
            instance,
            validated_data
    ):

        cls.events.append(
            "_create_post_save"
        )

        super()._create_post_save(
            instance,
            validated_data,
        )

    @classmethod
    def _update_post_save(
            cls,
            instance,
            validated_data
    ):

        cls.events.append(
            "_update_post_save"
        )

        super()._update_post_save(
            instance,
            validated_data,
        )

    @classmethod
    def _add_m2m_fields(
            cls,
            *,
            instance,
            validated_data
    ):

        cls.events.append(
            "_add_m2m_fields"
        )

        super()._add_m2m_fields(
            instance=instance,
            validated_data=validated_data,
        )

    @classmethod
    def _apply_m2m_updates(
            cls,
            *,
            instance,
            validated_data
    ):

        cls.events.append(
            "_apply_m2m_updates"
        )

        super()._apply_m2m_updates(
            instance=instance,
            validated_data=validated_data,
        )

    @classmethod
    def _m2m_non_empty_validation(cls, instance):

        cls.events.append(
            "_m2m_non_empty_validation"
        )

        super()._m2m_non_empty_validation(instance)
