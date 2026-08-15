import pytest

from apps.companies.selectors.company_email_selector import (
    CompanyEmailSelector,
)
from apps.core.common.types.filters import CompanyEmailQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestCompanyEmailSelectorList:

    def test_list_returns_only_user_emails(
            self,
            user1,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user2,
    ):

        queryset = CompanyEmailSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
            self,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailQueryFilter(
            workspace_id=(
                co_email1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            ),
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
        }

    def test_list_filters_by_company_id(
            self,
            co_email1_co1_ws1_user1,
            co_email1_co2_ws1_user1,
    ):

        filters = CompanyEmailQueryFilter(
            company_id=co_email1_co1_ws1_user1.company.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
        }

    def test_list_filters_by_email_id(
            self,
            co_email1_co1_ws1_user1,
    ):

        filters = CompanyEmailQueryFilter(
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
        }

    def test_list_applies_multiple_filters(
            self,
            co_email1_co1_ws1_user1,
    ):

        filters = CompanyEmailQueryFilter(
            workspace_id=(
                co_email1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            ),
            company_id=co_email1_co1_ws1_user1.company.pk,
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
        }

    def test_list_never_returns_foreign_email(
            self,
            user1,
            co_email1_co1_ws1_user2,
    ):

        filters = CompanyEmailQueryFilter(
            id=co_email1_co1_ws1_user2.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filters_match_nothing(
            self,
            user1,
    ):

        filters = CompanyEmailQueryFilter(
            id=999999,
        )

        queryset = CompanyEmailSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestCompanyEmailSelectorGet:

    def test_get_returns_company_email(
            self,
            user1,
            co_email1_co1_ws1_user1,
    ):

        company_email = CompanyEmailSelector.get(
            user=user1,
            obj_id=co_email1_co1_ws1_user1.pk,
        )

        assert company_email == co_email1_co1_ws1_user1

    def test_get_foreign_company_email_raises_resource_not_found(
            self,
            user1,
            co_email1_co1_ws1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanyEmailSelector.get(
                user=user1,
                obj_id=co_email1_co1_ws1_user2.pk,
            )

    def test_get_unknown_company_email_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanyEmailSelector.get(
                user=user1,
                obj_id=999999,
            )
