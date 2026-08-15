import pytest

from apps.companies.selectors.job_position_selector import (
    JobPositionSelector,
)

from apps.core.common.types.filters import (
    JobPositionQueryFilter,
)

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
)


@pytest.mark.django_db
class TestJobPositionSelectorList:
    """
    Covers:
    - S-03 Ownership Enforcement
    - S-05 Accessible Queryset
    - S-06 Query Filtering
    - S-12 Consistent list interface
    """

    def test_list_returns_only_accessible_job_positions(
            self,
            user1,
            job_position1_user1,
            job_position1_user2,
    ):

        queryset = JobPositionSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_position1_user1,
        }


    def test_list_returns_all_owned_job_positions(
            self,
            user1,
            job_position1_user1,
            job_pos1_co2_ws1_user1,
    ):

        queryset = JobPositionSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_position1_user1,
            job_pos1_co2_ws1_user1,
        }


    def test_list_filters_by_workspace_id(
            self,
            job_position1_user1,
            job_pos1_co1_ws2_user1,
    ):

        filters = JobPositionQueryFilter(
            workspace_id=(
                job_position1_user1
                .company
                .workspace
                .workspace_id
            ),
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            job_position1_user1,
        }


    def test_list_filters_by_company_id(
            self,
            job_position1_user1,
            job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionQueryFilter(
            company_id=job_position1_user1.company.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            job_position1_user1,
        }


    def test_list_filters_by_job_position_id(
            self,
            job_position1_user1,
            job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionQueryFilter(
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            job_position1_user1,
        }


    def test_list_applies_multiple_filters(
            self,
            job_position1_user1,
            job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionQueryFilter(
            workspace_id=(
                job_position1_user1
                .company
                .workspace
                .workspace_id
            ),
            company_id=job_position1_user1.company.pk,
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            job_position1_user1,
        }


    def test_list_does_not_return_foreign_position_even_with_matching_id(
            self,
            user1,
            job_position1_user2,
    ):

        filters = JobPositionQueryFilter(
            id=job_position1_user2.pk,
        )

        queryset = JobPositionSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


    def test_list_returns_empty_queryset_when_user_has_no_positions(
            self,
            user1,
    ):

        queryset = JobPositionSelector.list(
            user=user1,
        )

        assert list(queryset) == []


    def test_list_returns_empty_queryset_when_filter_matches_nothing(
            self,
            job_position1_user1,
    ):

        filters = JobPositionQueryFilter(
            id=999999,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert list(queryset) == []


    def test_list_returns_empty_queryset_when_multiple_filters_conflict(
            self,
            job_position1_user1,
            job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionQueryFilter(
            workspace_id=(
                job_position1_user1
                .company
                .workspace
                .workspace_id
            ),
            company_id=job_pos1_co2_ws1_user1.company.pk,
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestJobPositionSelectorGet:
    """
    Covers:
    - S-03 Ownership Enforcement
    - S-07 Exception Translation
    - S-12 Consistent get interface
    """

    def test_get_returns_accessible_job_position(
            self,
            user1,
            job_position1_user1,
    ):

        job_position = JobPositionSelector.get(
            user=user1,
            obj_id=job_position1_user1.pk,
        )

        assert job_position == job_position1_user1


    def test_get_foreign_position_raises_resource_not_found(
            self,
            user1,
            job_position1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobPositionSelector.get(
                user=user1,
                obj_id=job_position1_user2.pk,
            )


    def test_get_missing_position_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobPositionSelector.get(
                user=user1,
                obj_id=999999,
            )
