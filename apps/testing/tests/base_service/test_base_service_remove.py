import pytest

from apps.core.common.services.base_service import BaseService
from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class DummyRemoveService(BaseService):

    MODEL = DummyItem
    SELECTOR = DummyItemSelector

    CREATE_FIELDS = (
        "owner",
        "name",
    )

    SCALAR_UPDATABLE_FIELDS = ()

    M2M_UPDATABLE_FIELDS = ()

    REQUIRED_M2M_FIELDS = ()

    NON_EMPTY_M2M_FIELDS = ()

    M2M_OWNER_FIELD_MAP = {}

    calls = []

    @classmethod
    def _resolve_instance(cls, *, user, context):
        cls.calls.append("_resolve_instance")
        return context

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


@pytest.mark.django_db
def test_remove_executes_remove_workflow_in_contract_order(item1):

    DummyRemoveService.calls = []

    DummyRemoveService.remove(
        user=item1.owner,
        context=item1,
    )

    assert DummyRemoveService.calls == [
        "_resolve_instance",
    ]


@pytest.mark.django_db
def test_remove_deletes_instance(item1):

    pk = item1.pk

    DummyRemoveService.remove(
        user=item1.owner,
        context=item1,
    )

    assert not DummyItem.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_remove_calls_resolve_instance_once(item1):

    count = 0

    class Service(DummyRemoveService):

        @classmethod
        def _resolve_instance(cls, *, user, context):
            nonlocal count
            count += 1
            return context

    Service.remove(
        user=item1.owner,
        context=item1,
    )

    assert count == 1


@pytest.mark.django_db
def test_remove_returns_none(item1):

    result = DummyRemoveService.remove(
        user=item1.owner,
        context=item1,
    )

    assert result is None
