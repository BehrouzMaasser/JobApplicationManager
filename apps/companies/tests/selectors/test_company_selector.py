import pytest

from apps.companies.selectors.company_selector import CompanySelector
from apps.core.common.types.filters import CompanyQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestCompanySelectorList:

    def test_list_returns_only_user_companies(
            self,
            user1,
            co1_ws1_user1,
            co1_ws1_user2,
    ):

        queryset = CompanySelector.list(user=user1)

        assert set(queryset) == {
            co1_ws1_user1,
        }

    def test_list_filters_by_workspace(
            self,
            co1_ws1_user1,
            co1_ws2_user1,
    ):

        filters = CompanyQueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co1_ws1_user1,
        }

    def test_list_filters_by_company_id(
            self,
            co1_ws1_user1,
            co2_ws1_user1,
    ):

        filters = CompanyQueryFilter(
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co1_ws1_user1,
        }

    def test_list_applies_multiple_filters(
            self,
            co1_ws1_user1,
            co2_ws1_user1,
    ):

        filters = CompanyQueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co1_ws1_user1,
        }

    def test_list_never_returns_foreign_company(
            self,
            user1,
            co1_ws1_user2,
    ):

        filters = CompanyQueryFilter(
            id=co1_ws1_user2.pk,
        )

        queryset = CompanySelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filters_match_nothing(
            self,
            co1_ws1_user1,
    ):

        filters = CompanyQueryFilter(
            id=999999,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestCompanySelectorGet:

    def test_get_returns_company(
            self,
            user1,
            co1_ws1_user1,
    ):

        company = CompanySelector.get(
            user=user1,
            obj_id=co1_ws1_user1.pk,
        )

        assert company == co1_ws1_user1

    def test_get_foreign_company_raises_resource_not_found(
            self,
            user1,
            co1_ws1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanySelector.get(
                user=user1,
                obj_id=co1_ws1_user2.pk,
            )

    def test_get_unknown_company_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanySelector.get(
                user=user1,
                obj_id=999999,
            )
