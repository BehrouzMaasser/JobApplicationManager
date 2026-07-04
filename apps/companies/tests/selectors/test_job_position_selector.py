import pytest

from apps.companies.selectors.job_position_selector import JobPositionSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
)


@pytest.mark.django_db
class TestJobPositionSelectorList:

    def test_list_returns_only_user_owned_positions(
        self,
        user1,
        job_position1_user1,
        job_position1_user2,
    ):

        queryset = JobPositionSelector.list(user=user1)

        assert set(queryset) == {job_position1_user1}

    def test_list_without_filters_returns_all_owned_positions(
        self,
        user1,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        queryset = JobPositionSelector.list(user=user1)

        assert set(queryset) == {
            job_position1_user1,
            job_pos1_co2_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
        self,
        job_position1_user1,
        job_pos1_co1_ws2_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=job_position1_user1.company.workspace.workspace_id,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {job_position1_user1}

    def test_list_filters_by_company_id(
        self,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            company_id=job_position1_user1.company.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {job_position1_user1}

    def test_list_filters_by_position_id(
        self,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {job_position1_user1}

    def test_list_applies_multiple_filters(
        self,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=job_position1_user1.company.workspace.workspace_id,
            company_id=job_position1_user1.company.pk,
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {job_position1_user1}

    def test_list_never_returns_foreign_position_even_with_matching_id(
        self,
        user1,
        job_position1_user2,
    ):

        filters = JobPositionSelector.QueryFilter(
            id=job_position1_user2.pk,
        )

        queryset = JobPositionSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_positions(
        self,
        user1,
    ):

        queryset = JobPositionSelector.list(user=user1)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        job_position1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            id=999999,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=job_position1_user1.company.workspace.workspace_id,
            company_id=job_pos1_co2_ws1_user1.company.pk,
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=job_position1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestJobPositionSelectorGet:

    def test_get_returns_position_for_owner(
        self,
        user1,
        job_position1_user1,
    ):

        job_position = JobPositionSelector.get(
            user=user1,
            job_position_id=job_position1_user1.pk,
        )

        assert job_position == job_position1_user1

    def test_get_raises_when_position_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):
            JobPositionSelector.get(
                user=user1,
                job_position_id=999999,
            )

    def test_get_raises_when_position_belongs_to_another_user(
        self,
        user1,
        job_position1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            JobPositionSelector.get(
                user=user1,
                job_position_id=job_position1_user2.pk,
            )
