import uuid
from unittest.mock import patch

import pytest

from apps.core.common.selectors.base_selector import BaseSelector
from apps.core.exceptions.exceptions import (
    InfraStructureViolationError,
    ResourceNotFoundError,
)
from apps.workspaces.models import Workspace


pytest_plugins = [
    "apps.workspaces.tests.conftest",
]


class DummyWorkspaceSelector(BaseSelector[Workspace]):

    MODEL = Workspace
    RESOURCE_NAME = "Workspace"
    LOOKUP_FIELD = "workspace_id"
    OWNER_PATH = "owner"


class NoOwnerSelector(BaseSelector[Workspace]):

    MODEL = Workspace
    RESOURCE_NAME = "Workspace"
    LOOKUP_FIELD = "workspace_id"


# -----------------------------------------------------------------------------
# Contract: Selector Configuration (G-01, G-02)
# -----------------------------------------------------------------------------


class TestBaseSelectorConfiguration:

    def test_selector_with_required_configuration_is_created(self):

        class ValidSelector(BaseSelector[Workspace]):

            MODEL = Workspace
            RESOURCE_NAME = "Workspace"
            LOOKUP_FIELD = "workspace_id"
            OWNER_PATH = "owner"

        assert ValidSelector.MODEL is Workspace

    def test_selector_without_model_raises_type_error(self):

        with pytest.raises(
            TypeError,
            match="must define MODEL",
        ):

            class InvalidSelector(BaseSelector[Workspace]):

                RESOURCE_NAME = "Workspace"
                LOOKUP_FIELD = "workspace_id"
                OWNER_PATH = "owner"

    def test_selector_without_resource_name_raises_type_error(self):

        with pytest.raises(
            TypeError,
            match="must define RESOURCE_NAME",
        ):

            class InvalidSelector(BaseSelector[Workspace]):

                MODEL = Workspace
                LOOKUP_FIELD = "workspace_id"
                OWNER_PATH = "owner"

    def test_selector_without_lookup_field_raises_type_error(self):

        with pytest.raises(
            TypeError,
            match="must define LOOKUP_FIELD",
        ):

            class InvalidSelector(BaseSelector[Workspace]):

                MODEL = Workspace
                RESOURCE_NAME = "Workspace"
                OWNER_PATH = "owner"

    def test_base_selector_can_be_defined_without_configuration(self):

        assert BaseSelector.MODEL is None
        assert BaseSelector.RESOURCE_NAME is None
        assert BaseSelector.LOOKUP_FIELD is None


# -----------------------------------------------------------------------------
# Contract: S-04 Base Queryset
# Contract: S-05 Accessible Queryset
# Contract: S-03 Ownership Enforcement
# -----------------------------------------------------------------------------


@pytest.mark.django_db
class TestBaseSelectorQuerysets:

    def test_base_queryset_returns_all_objects(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        queryset = DummyWorkspaceSelector.base_queryset()

        assert set(queryset) == {
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
        }

    def test_accessible_queryset_returns_only_owned_objects(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        queryset = DummyWorkspaceSelector.accessible_queryset(
            user=workspace1_user1.owner,
        )

        assert set(queryset) == {
            workspace1_user1,
            workspace2_user1,
        }

    def test_accessible_queryset_without_owner_path_returns_empty_queryset(
            self,
            workspace1_user1,
    ):

        queryset = NoOwnerSelector.accessible_queryset(
            user=workspace1_user1.owner,
        )

        assert list(queryset) == []


# -----------------------------------------------------------------------------
# Contract: S-07 Exception Translation
# Contract: S-10 Return Types
# -----------------------------------------------------------------------------


@pytest.mark.django_db
class TestBaseSelectorGet:

    def test_get_returns_object(
            self,
            workspace1_user1,
    ):

        workspace = DummyWorkspaceSelector.get(
            user=workspace1_user1.owner,
            obj_id=workspace1_user1.workspace_id,
        )

        assert workspace == workspace1_user1

    def test_get_inaccessible_object_raises_resource_not_found(
            self,
            user1,
            workspace1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            DummyWorkspaceSelector.get(
                user=user1,
                obj_id=workspace1_user2.workspace_id,
            )

    def test_get_missing_object_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            DummyWorkspaceSelector.get(
                user=user1,
                obj_id=uuid.uuid4(),
            )

    def test_get_translates_unexpected_exception_to_infrastructure_violation(
            self,
            workspace1_user1,
    ):

        with patch.object(
            DummyWorkspaceSelector,
            "accessible_queryset",
            side_effect=RuntimeError("boom"),
        ):

            with pytest.raises(InfraStructureViolationError):

                DummyWorkspaceSelector.get(
                    user=workspace1_user1.owner,
                    obj_id=workspace1_user1.workspace_id,
                )


# -----------------------------------------------------------------------------
# Contract: S-06 Query Filtering
# Contract: S-12 Consistent Public API
# -----------------------------------------------------------------------------


@pytest.mark.django_db
class TestBaseSelectorList:

    def test_list_returns_accessible_queryset(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        queryset = DummyWorkspaceSelector.list(
            user=workspace1_user1.owner,
        )

        assert set(queryset) == {
            workspace1_user1,
            workspace2_user1,
        }

    def test_default_apply_filters_returns_original_queryset(
            self,
            workspace1_user1,
            workspace2_user1,
    ):

        queryset = DummyWorkspaceSelector.base_queryset()

        filtered = DummyWorkspaceSelector.apply_filters(
            queryset=queryset,
            filters=object(),
        )

        assert filtered is queryset
