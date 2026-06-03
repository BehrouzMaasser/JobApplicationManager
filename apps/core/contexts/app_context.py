from dataclasses import dataclass


@dataclass(frozen=True)
class AppContext:

    workspace_id: str | None = None
    company_id: int | None = None
    email_id: int | None = None
    note_id: int | None = None
    position_id: int | None = None
