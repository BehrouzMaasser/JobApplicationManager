from dataclasses import dataclass

from apps.companies.services.contexts.company_context import CompanyChildContext


@dataclass
class JobApplicationContext(CompanyChildContext):

    job_position_id: int


@dataclass
class JobApplicationChildContext(JobApplicationContext):

    job_application_id: int
