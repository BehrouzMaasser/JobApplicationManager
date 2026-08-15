import pytest

from apps.companies.selectors.company_note_selector import (
    CompanyNoteSelector,
)
from apps.core.common.types.filters import CompanyNoteQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestCompanyNoteSelectorList:

    def test_list_returns_only_user_notes(
            self,
            user1,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user2,
    ):

        queryset = CompanyNoteSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
            self,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws2_user1,
    ):

        filters = CompanyNoteQueryFilter(
            workspace_id=(
                co_note1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            ),
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
        }

    def test_list_filters_by_company_id(
            self,
            co_note1_co1_ws1_user1,
            co_note1_co2_ws1_user1,
    ):

        filters = CompanyNoteQueryFilter(
            company_id=co_note1_co1_ws1_user1.company.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
        }

    def test_list_filters_by_note_id(
            self,
            co_note1_co1_ws1_user1,
            co_note1_co2_ws1_user1,
    ):

        filters = CompanyNoteQueryFilter(
            id=co_note1_co1_ws1_user1.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
        }

    def test_list_applies_multiple_filters(
            self,
            co_note1_co1_ws1_user1,
    ):

        filters = CompanyNoteQueryFilter(
            workspace_id=(
                co_note1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            ),
            company_id=co_note1_co1_ws1_user1.company.pk,
            id=co_note1_co1_ws1_user1.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
        }

    def test_list_never_returns_foreign_note(
            self,
            user1,
            co_note1_co1_ws1_user2,
    ):

        filters = CompanyNoteQueryFilter(
            id=co_note1_co1_ws1_user2.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filters_match_nothing(
            self,
            user1,
    ):

        filters = CompanyNoteQueryFilter(
            id=999999,
        )

        queryset = CompanyNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestCompanyNoteSelectorGet:

    def test_get_returns_company_note(
            self,
            user1,
            co_note1_co1_ws1_user1,
    ):

        company_note = CompanyNoteSelector.get(
            user=user1,
            obj_id=co_note1_co1_ws1_user1.pk,
        )

        assert company_note == co_note1_co1_ws1_user1

    def test_get_foreign_company_note_raises_resource_not_found(
            self,
            user1,
            co_note1_co1_ws1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanyNoteSelector.get(
                user=user1,
                obj_id=co_note1_co1_ws1_user2.pk,
            )

    def test_get_unknown_company_note_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            CompanyNoteSelector.get(
                user=user1,
                obj_id=999999,
            )
