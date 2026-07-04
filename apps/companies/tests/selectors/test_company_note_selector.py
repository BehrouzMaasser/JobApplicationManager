import pytest

from apps.companies.selectors.company_note_selector import CompanyNoteSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
)


@pytest.mark.django_db
class TestCompanyNoteSelectorList:

    def test_list_returns_only_user_owned_notes(
        self,
        user1,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user2,
    ):

        queryset = CompanyNoteSelector.list(user=user1)

        assert set(queryset) == {co_note1_co1_ws1_user1}

    def test_list_without_filters_returns_all_owned_notes(
        self,
        user1,
        co_note1_co1_ws1_user1,
        co_note1_co2_ws1_user1,
    ):

        queryset = CompanyNoteSelector.list(user=user1)

        assert set(queryset) == {
            co_note1_co1_ws1_user1,
            co_note1_co2_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws2_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_note1_co1_ws1_user1}

    def test_list_filters_by_company_id(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co2_ws1_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            company_id=co_note1_co1_ws1_user1.company.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_note1_co1_ws1_user1}

    def test_list_filters_by_note_id(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co2_ws1_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            id=co_note1_co1_ws1_user1.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_note1_co1_ws1_user1}

    def test_list_applies_multiple_filters(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co2_ws1_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
            company_id=co_note1_co1_ws1_user1.company.pk,
            id=co_note1_co1_ws1_user1.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_note1_co1_ws1_user1}

    def test_list_never_returns_foreign_note_even_with_matching_id(
        self,
        user1,
        co_note1_co1_ws1_user2,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            id=co_note1_co1_ws1_user2.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_notes(
        self,
        user1,
    ):

        queryset = CompanyNoteSelector.list(user=user1)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        co_note1_co1_ws1_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            id=999999,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws2_user1,
    ):

        filters = CompanyNoteSelector.QueryFilter(
            workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
            company_id=co_note1_co1_ws2_user1.company.pk,
        )

        queryset = CompanyNoteSelector.list(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestCompanyNoteSelectorGet:

    def test_get_returns_note_for_owner(
        self,
        user1,
        co_note1_co1_ws1_user1,
    ):

        company_note = CompanyNoteSelector.get(
            user=user1,
            company_note_id=co_note1_co1_ws1_user1.pk,
        )

        assert company_note == co_note1_co1_ws1_user1

    def test_get_raises_when_note_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):
            CompanyNoteSelector.get(
                user=user1,
                company_note_id=999999,
            )

    def test_get_raises_when_note_belongs_to_another_user(
        self,
        user1,
        co_note1_co1_ws1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            CompanyNoteSelector.get(
                user=user1,
                company_note_id=co_note1_co1_ws1_user2.pk,
            )
