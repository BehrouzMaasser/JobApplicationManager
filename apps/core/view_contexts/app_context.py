from dataclasses import dataclass


@dataclass(frozen=True)
class AppContext:

    workspace_id: str | None = None
    company_id: int | None = None
    email_id: int | None = None
    note_id: int | None = None
    position_id: int | None = None
    application_id: int | None = None
    application_note_id: int | None = None
    companies_list_url: str | None = None
    applications_list_url: str | None = None
    application_notes_list_url: str | None = None
    positions_list_url: str | None = None
    company_emails_list_url: str | None = None
    company_notes_list_url: str | None = None
