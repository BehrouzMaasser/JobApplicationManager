import pytest

from apps.companies.selectors.job_position_selector import JobPositionSelector


@pytest.mark.django_db
class TestJobPositionSelector:

    def test_list_returns_only_user_owned_positions(
        self,
        user,
        job_position1_user1,
        job_position1_user2,
    ):

        queryset = JobPositionSelector.list(user=user)

        assert job_position1_user1 in queryset
        assert job_position1_user2 not in queryset
        assert queryset.count() == 1

    def test_list_without_filters_returns_all_owned_positions(
        self,
        user,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        queryset = JobPositionSelector.list(user=user)

        assert job_position1_user1 in queryset
        assert job_pos1_co2_ws1_user1 in queryset
        assert queryset.count() == 2

    def test_list_filters_by_workspace_id(
        self,
        user,
        workspace_user1,
        job_position1_user1,
        job_pos1_co1_ws2_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=workspace_user1.workspace_id,
        )

        queryset = JobPositionSelector.list(
            user=user,
            filters=filters,
        )

        assert job_position1_user1 in queryset
        assert job_pos1_co1_ws2_user1 not in queryset
        assert queryset.count() == 1

    def test_list_filters_by_company_id(
        self,
        user,
        co1_ws1_user1,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            company_id=co1_ws1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=user,
            filters=filters,
        )

        assert job_position1_user1 in queryset
        assert job_pos1_co2_ws1_user1 not in queryset
        assert queryset.count() == 1

    def test_list_filters_by_position_id(
        self,
        user,
        job_position1_user1,
        job_pos1_co2_ws1_user1,
    ):

        filters = JobPositionSelector.QueryFilter(
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=user,
            filters=filters,
        )

        assert job_position1_user1 in queryset
        assert job_pos1_co2_ws1_user1 not in queryset
        assert queryset.count() == 1

    def test_list_applies_multiple_filters(
        self,
        user,
        job_position1_user1,
        job_pos1_co2_ws1_user1
    ):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=job_position1_user1.company.workspace.workspace_id,
            company_id=job_position1_user1.company.pk,
            id=job_position1_user1.pk,
        )

        queryset = JobPositionSelector.list(
            user=user,
            filters=filters,
        )

        assert list(queryset) == [job_position1_user1]

    def test_list_never_returns_foreign_position_even_with_matching_id(
        self,
        user,
        job_position1_user2,
    ):

        filters = JobPositionSelector.QueryFilter(
            id=job_position1_user2.pk,
        )

        queryset = JobPositionSelector.list(
            user=user,
            filters=filters,
        )

        assert queryset.count() == 0
