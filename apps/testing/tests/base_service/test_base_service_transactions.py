import pytest

from apps.core.common.services.base_service import BaseService
from apps.core.exceptions.exceptions import InfrastructureViolationError

from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class DummyTransactionService(BaseService):

    MODEL = DummyItem
    SELECTOR = DummyItemSelector

    CREATE_FIELDS = (
        "owner",
        "name",
    )

    SCALAR_UPDATABLE_FIELDS = (
        "name",
    )

    M2M_UPDATABLE_FIELDS = ()

    REQUIRED_M2M_FIELDS = ()

    NON_EMPTY_M2M_FIELDS = ()

    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(cls, user, context):
        return {
            "owner": user,
        }

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


@pytest.mark.django_db
def test_create_rolls_back_when_post_save_fails(user1):

    class Service(DummyTransactionService):

        @classmethod
        def _create_post_save(
            cls,
            instance,
            validated_data,
        ):
            raise RuntimeError(
                "post save failure"
            )

    with pytest.raises(InfrastructureViolationError):

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Rollback",
            },
        )

    assert not DummyItem.objects.filter(
        name="Rollback",
    ).exists()


@pytest.mark.django_db
def test_update_rolls_back_when_post_save_fails(item1):

    old_name = item1.name

    class Service(DummyTransactionService):

        @classmethod
        def _resolve_instance(cls, *, user, context):
            return item1

        @classmethod
        def _update_post_save(
            cls,
            instance,
            validated_data,
        ):
            raise RuntimeError(
                "post save failure"
            )

    with pytest.raises(InfrastructureViolationError):

        Service.update(
            user=item1.owner,
            context=item1,
            validated_data={
                "name": "Rollback",
            },
        )

    item1.refresh_from_db()

    assert item1.name == old_name
