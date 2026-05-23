from dataclasses import dataclass


@dataclass
class CompanyContext:

    id: int | None
    workspace_id: str


@dataclass
class CompanyChildContext(CompanyContext):

    company_id: int
