import pytest

from django.contrib.auth import get_user_model

from apps.companies.models import (
    JobPosition,
    CompanyEmail,
    Company,
    CompanyNote,
    JobBenefit,
    JobTask,
    JobRequirement,
    EmploymentType,
    JobSite
)

from apps.core.common.contexts.contexts import (
    JobApplicationContext,
    JobApplicationChildContext,
    CompanyContext,
    CompanyChildContext
)

User = get_user_model()


@pytest.fixture
def user1(db):
    return User.objects.create_user(email="user1@gmail.com", password="pass")


@pytest.fixture
def user2(db):
    return User.objects.create_user(email="user2@gmail.com", password="pass")


@pytest.fixture
def api_client():

    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user1):

    api_client.force_authenticate(user=user1)
    return api_client


@pytest.fixture
def base_api_url_path():

    return "/api/v1/"


# ============================================================================
# Workspaces
# ============================================================================

from apps.workspaces.models import Workspace


@pytest.fixture
def workspace1_user1(db, user1):
    return Workspace.objects.create(
        name="Test Workspace 1",
        owner=user1
    )


@pytest.fixture
def workspace2_user1(db, user1):
    return Workspace.objects.create(
        name="Test Workspace 2",
        owner=user1
    )


@pytest.fixture
def workspace1_user2(db, user2):
    return Workspace.objects.create(
        name="Test Workspace 1",
        owner=user2
    )


@pytest.fixture
def workspace2_user2(db, user2):
    return Workspace.objects.create(
        name="Test Workspace 2",
        owner=user2
    )


# ============================================================================
# Companies
# ============================================================================


@pytest.fixture
def co1_ws1_user1(db, workspace1_user1):

    return Company.objects.create(
        name="co1",
        workspace=workspace1_user1,
    )


@pytest.fixture
def co1_ws2_user1(db, workspace2_user1):

    return Company.objects.create(
        name="co1",
        workspace=workspace2_user1,
    )


@pytest.fixture
def co2_ws1_user1(db, workspace1_user1):

    return Company.objects.create(
        name="co2",
        workspace=workspace1_user1,
    )


@pytest.fixture
def co1_ws1_user2(db, workspace1_user2):

    return Company.objects.create(
        name="co2",
        workspace=workspace1_user2,
    )


@pytest.fixture
def co1_ws1_user1_context_with_id(db, co1_ws1_user1):

    return CompanyContext(
        id=co1_ws1_user1.id,
        workspace_id=co1_ws1_user1.workspace.workspace_id
    )


@pytest.fixture
def co1_ws1_user1_context_no_id(db, workspace1_user1):

    return CompanyContext(id=None, workspace_id=workspace1_user1.workspace_id)


@pytest.fixture
def co1_child_context_ws1_user1_no_id(db, co1_ws1_user1_context_with_id):

    return CompanyChildContext(
        id=None,
        workspace_id=co1_ws1_user1_context_with_id.workspace_id,
        company_id=co1_ws1_user1_context_with_id.id
    )


@pytest.fixture
def co_note1_co1_ws1_user1_valid_data():

    return {"title": "Title", "content": "Some Content"}


@pytest.fixture
def co_note1_co1_ws1_user1_updated_valid_data():

    return {"title": "Title Updated", "content": "Some Content Updated"}


@pytest.fixture
def co_note1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyNote.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co1_ws1_user2(db, co1_ws1_user2):

    return CompanyNote.objects.create(
        company=co1_ws1_user2,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co2_ws1_user1(db, co2_ws1_user1):

    return CompanyNote.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co1_ws2_user1(db, co1_ws2_user1):

    return CompanyNote.objects.create(
        company=co1_ws2_user1,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co1_ws1_user1_context_with_id(db, co_note1_co1_ws1_user1):

    return CompanyChildContext(
        id=co_note1_co1_ws1_user1.id,
        workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=co_note1_co1_ws1_user1.company.id
    )


# Email Fixtures:

@pytest.fixture
def co_email1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co1_ws1_user2(db, co1_ws1_user2):

    return CompanyEmail.objects.create(
        company=co1_ws1_user2,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co1_ws2_user1(db, co1_ws2_user1):

    return CompanyEmail.objects.create(
        company=co1_ws2_user1,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co2_ws1_user1(db, co2_ws1_user1):

    return CompanyEmail.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co1_ws1_user1_context_with_id(db, co_email1_co1_ws1_user1):

    return CompanyChildContext(
        id=co_email1_co1_ws1_user1.id,
        workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=co_email1_co1_ws1_user1.company.id
    )


# Job Benefit Fixtures:

@pytest.fixture
def job_benefit1_user1_valid_data():

    return {"name": "Name1", "description": "Some Description"}


@pytest.fixture
def job_benefit1_user1_updated_valid_data():

    return {"name": "Name1 Updated", "description": "Some Description Updated"}


@pytest.fixture
def job_benefit1_user1(db, user1):

    return JobBenefit.objects.create(
        user=user1,
        name="Name1",
        description="Description1",
    )


@pytest.fixture
def job_benefit2_user1(db, user1):

    return JobBenefit.objects.create(
        user=user1,
        name="Name2",
        description="Description2",
    )


@pytest.fixture
def job_benefit1_user2(db, user2):

    return JobBenefit.objects.create(
        user=user2,
        name="Name1",
        description="Description1",
    )

# Job Task Fixtures:


@pytest.fixture
def job_task1_user1_valid_data():

    return {"title": "Title1", "description": "Description1"}


@pytest.fixture
def job_task1_user1_updated_valid_data():

    return {"title": "Title1 Updated", "description": "Description1 Updated"}


@pytest.fixture
def job_task1_user1(db, user1):

    return JobTask.objects.create(
        user=user1,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_task1_user2(db, user2):

    return JobTask.objects.create(
        user=user2,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_task2_user1(db, user1):

    return JobTask.objects.create(
        user=user1,
        title="Title2",
        description="Descriptions2",
    )


# Job Requirement Fixtures:

@pytest.fixture
def job_requirement1_user1_valid_data():

    return {"title": "Title1", "description": "Description1"}


@pytest.fixture
def job_requirement1_user1_updated_valid_data():

    return {"title": "Title1 Updated", "description": "Description1 Updated"}


@pytest.fixture
def job_requirement1_user1(db, user1):

    return JobRequirement.objects.create(
        user=user1,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_requirement1_user2(db, user2):

    return JobRequirement.objects.create(
        user=user2,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_requirement2_user1(db, user1):

    return JobRequirement.objects.create(
        user=user1,
        title="Title2",
        description="Description2",
    )


# Employment Type Fixtures:

@pytest.fixture
def empl_type1(db):

    return EmploymentType.objects.create(
        name="Type1",
    )


@pytest.fixture
def empl_type2(db):

    return EmploymentType.objects.create(
        name="Type2",
    )


# Job Site Fixtures:

@pytest.fixture
def job_site1(db):

    return JobSite.objects.create(
        name="Site1",
    )


@pytest.fixture
def job_site2(db):

    return JobSite.objects.create(
        name="Site2",
    )


# Job Position Fixtures:

@pytest.fixture
def job_position1_user1(
        db,
        co1_ws1_user1,
        empl_type1,
        job_requirement1_user1,
        job_task1_user1,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task1_user1.id])
    job_position.requirements.set([job_requirement1_user1.id])

    return job_position


@pytest.fixture
def job_position1_user2(
        db,
        co1_ws1_user2,
        empl_type1,
        job_requirement1_user2,
        job_task1_user2,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co1_ws1_user2,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task1_user2.id])
    job_position.requirements.set([job_requirement1_user2.id])

    return job_position


@pytest.fixture
def job_pos1_co2_ws1_user1(
        db,
        co2_ws1_user1,
        empl_type1,
        job_requirement1_user1,
        job_task1_user1,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task1_user1.id])
    job_position.requirements.set([job_requirement1_user1.id])

    return job_position


@pytest.fixture
def job_pos1_co1_ws2_user1(
        db,
        co1_ws2_user1,
        empl_type1,
        job_requirement1_user1,
        job_task1_user1,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co1_ws2_user1,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task1_user1.id])
    job_position.requirements.set([job_requirement1_user1.id])

    return job_position


@pytest.fixture
def job_position1_context(db, job_position1_user1):

    return CompanyChildContext(
        id=job_position1_user1.id,
        workspace_id=job_position1_user1.company.workspace.workspace_id,
        company_id=job_position1_user1.company.id
    )


@pytest.fixture
def job_pos_user1_valid_data(
        empl_type1,
        job_site1,
        job_task1_user1,
        job_requirement1_user1
):

    return {
        "title": "Title1",
        "description": "Description1",
        "employment_types": [empl_type1],
        "job_sites": [job_site1],
        "tasks": [job_task1_user1],
        "requirements": [job_requirement1_user1],
    }


@pytest.fixture
def job_pos_user1_views_valid_data(
        empl_type1,
        job_site1,
        job_task1_user1,
        job_requirement1_user1
):

    return {
        "title": "Title1",
        "description": "Description1",
        "employment_types": [empl_type1.pk],
        "job_sites": [job_site1.pk],
        "tasks": [job_task1_user1.pk],
        "requirements": [job_requirement1_user1.pk],
    }


@pytest.fixture
def job_pos_user1_views_updated_valid_data(
        empl_type2,
        job_site2,
        job_task2_user1,
        job_requirement2_user1
):

    return {
        "title": "Title1 Updated",
        "description": "Description1 Updated",
        "employment_types": [empl_type2.pk],
        "job_sites": [job_site2.pk],
        "tasks": [job_task2_user1.pk],
        "requirements": [job_requirement2_user1.pk],
    }


@pytest.fixture
def job_pos_user1_api_valid_data(
        empl_type1,
        job_site1,
        job_task1_user1,
        job_requirement1_user1
):

    return {
        "title": "Title1",
        "description": "Description1",
        "employment_types": [empl_type1.id],
        "job_sites": [job_site1.id],
        "tasks": [job_task1_user1.id],
        "requirements": [job_requirement1_user1.id],
    }


@pytest.fixture
def job_pos_user1_updated_valid_data(
        empl_type1,
        empl_type2,
        job_site2,
        job_task2_user1,
        job_requirement2_user1,
        job_benefit1_user1,
):

    return {
        "title": "Title1 Edited",
        "description": "Description1 Edited",
        "employment_types": [empl_type1, empl_type2],
        "job_sites": [job_site2],
        "tasks": [job_task2_user1],
        "requirements": [job_requirement2_user1],
        "benefits": [job_benefit1_user1],
    }


@pytest.fixture
def job_pos_user1_api_updated_valid_data(
        empl_type1,
        empl_type2,
        job_site2,
        job_task2_user1,
        job_requirement2_user1,
        job_benefit1_user1,
):

    return {
        "title": "Title1 Edited",
        "description": "Description1 Edited",
        "employment_types": [empl_type1.id, empl_type2.id],
        "job_sites": [job_site2.id],
        "tasks": [job_task2_user1.id],
        "requirements": [job_requirement2_user1.id],
        "benefits": [job_benefit1_user1.id],
    }




# ============================================================================
# Applications
# ============================================================================


from apps.applications.models import (
    ApplicationStatus,
    JobApplication,
    JobApplicationNote
)

# ----------------------*****---------------------


# Fixtures:

# Status Fixtures:

@pytest.fixture
def status1(db):

    return ApplicationStatus.objects.create(label="Pending", order=1)


@pytest.fixture
def status2(db):

    return ApplicationStatus.objects.create(label="Interview", order=2)

# ----------------------*****---------------------


# Job Position Fixtures:

@pytest.fixture
def job_position1_co1_ws1_user1(db, co1_ws1_user1):

    return JobPosition.objects.create(
        title="Title 1",
        company=co1_ws1_user1,
        description="Description 1",
    )


@pytest.fixture
def job_position1_co1_ws1_user1_with_m2m(
        db,
        job_position1_co1_ws1_user1,
        empl_type1,
        job_site1,
        job_task1_user1,
        job_requirement1_user1
):

    job_position1_co1_ws1_user1.employment_types.set([empl_type1.id])
    job_position1_co1_ws1_user1.job_sites.set([job_site1.id])
    job_position1_co1_ws1_user1.tasks.set([job_task1_user1.id])
    job_position1_co1_ws1_user1.requirements.set([job_requirement1_user1.id])

    return job_position1_co1_ws1_user1


@pytest.fixture
def job_position1_co1_ws1_user2(db, co1_ws1_user2):

    return JobPosition.objects.create(
        title="Title 1",
        company=co1_ws1_user2,
        description="Description 1",
    )


@pytest.fixture
def job_position1_co1_ws2_user1(db, co1_ws2_user1):

    return JobPosition.objects.create(
        title="Title 1",
        company=co1_ws2_user1,
        description="Description 1",
    )


@pytest.fixture
def job_position2_co1_ws1_user1(db, co1_ws1_user1):

    return JobPosition.objects.create(
        title="Title 2",
        company=co1_ws1_user1,
        description="Description 2"
    )


@pytest.fixture
def job_position1_co2_ws1_user1(db, co2_ws1_user1):

    return JobPosition.objects.create(
        title="Title 1",
        company=co2_ws1_user1,
        description="Description 1",
    )

# ----------------------*****---------------------


# Company Email Fixtures:

@pytest.fixture
def email1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        email="email1@gmail.com",
        title="Title 1",
    )


@pytest.fixture
def email2_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        email="email2@gmail.com",
        title="Title 2",
    )

# ----------------------*****---------------------


# Job Application Fixtures:

@pytest.fixture
def job_application1_valid_data(status1, email1_co1_ws1_user1):

    return {
        "status": status1,
        "emails": [email1_co1_ws1_user1],
    }


@pytest.fixture
def job_application1_api_valid_data(status1, email1_co1_ws1_user1):

    return {
        "status": status1.id,
    }


@pytest.fixture
def job_application1_valid_data_updated(
        status2,
        email1_co1_ws1_user1,
        email2_co1_ws1_user1,
):

    return {
        "status": status2,
        "emails": [email1_co1_ws1_user1, email2_co1_ws1_user1],
    }


@pytest.fixture
def job_application1_api_valid_data_updated(
        status2,
        email1_co1_ws1_user1,
        email2_co1_ws1_user1,
):

    return {
        "status": status2.id,
        "emails": [email1_co1_ws1_user1.id, email2_co1_ws1_user1.id],
    }


@pytest.fixture
def job_application1(db, job_position1_co1_ws1_user1, status1):

    app = JobApplication.objects.create(
        owner=job_position1_co1_ws1_user1.company.workspace.owner,
        workspace=job_position1_co1_ws1_user1.company.workspace,
        job_position=job_position1_co1_ws1_user1,
        status=status1,
    )

    return app


@pytest.fixture
def job_app1_pos1_co1_ws2_user1(db, job_position1_co1_ws2_user1, status1):

    app = JobApplication.objects.create(
        owner=job_position1_co1_ws2_user1.company.workspace.owner,
        workspace=job_position1_co1_ws2_user1.company.workspace,
        job_position=job_position1_co1_ws2_user1,
        status=status1,
    )

    return app


@pytest.fixture
def job_app1_pos1_co2_ws1_user1(db, job_position1_co2_ws1_user1, status1):

    app = JobApplication.objects.create(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
    )

    return app


@pytest.fixture
def job_app1_pos2_co1_ws1_user1(db, job_position2_co1_ws1_user1, status1):

    app = JobApplication.objects.create(
        owner=job_position2_co1_ws1_user1.company.workspace.owner,
        workspace=job_position2_co1_ws1_user1.company.workspace,
        job_position=job_position2_co1_ws1_user1,
        status=status1,
    )

    return app


@pytest.fixture
def job_app1_pos1_co1_ws1_user2(db, job_position1_co1_ws1_user2, status1):

    app = JobApplication.objects.create(
        owner=job_position1_co1_ws1_user2.company.workspace.owner,
        workspace=job_position1_co1_ws1_user2.company.workspace,
        job_position=job_position1_co1_ws1_user2,
        status=status1,
    )

    return app


@pytest.fixture
def job_application1_context(db, job_application1):

    return JobApplicationContext(
        id=job_application1.id,
        workspace_id=job_application1.job_position.company.workspace.workspace_id,
        company_id=job_application1.job_position.company.id,
        job_position_id=job_application1.job_position.id,
    )


@pytest.fixture
def job_application_context_with_no_id(db, job_position1_co1_ws1_user1):

    return JobApplicationContext(
        id=None,
        workspace_id=job_position1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=job_position1_co1_ws1_user1.company.id,
        job_position_id=job_position1_co1_ws1_user1.id,
    )


@pytest.fixture
def job_application2(db, job_position1_co2_ws1_user1, status1):

    app = JobApplication.objects.create(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
    )

    return app

# ----------------------*****---------------------


# Application Note Fixtures:

@pytest.fixture
def app_note1_valid_data():

    return {"title": "Job Application Title Test 1", "content": "Test Content 1"}


@pytest.fixture
def app_note1_valid_data_updated():

    return {
        "title": "Job Application Title Test 1 Edited",
        "content": "Test Content 1 Edited"
    }


@pytest.fixture
def app_note1(db, job_application1):

    return JobApplicationNote.objects.create(
        job_application=job_application1,
        title="Title 1",
        content="Content",
    )


@pytest.fixture
def app_note2(db, job_app1_pos1_co1_ws2_user1):

    return JobApplicationNote.objects.create(
        job_application=job_app1_pos1_co1_ws2_user1,
        title="Title 1",
        content="Content",
    )


@pytest.fixture
def app_note1_user2(db, job_app1_pos1_co1_ws1_user2):

    return JobApplicationNote.objects.create(
        job_application=job_app1_pos1_co1_ws1_user2,
        title="Title 1",
        content="Content",
    )


@pytest.fixture
def app_note1_context_with_no_id(db, app_note1):

    return JobApplicationChildContext(
        id=None,
        workspace_id=app_note1.job_application.workspace.workspace_id,
        company_id=app_note1.job_application.job_position.company.id,
        job_position_id=app_note1.job_application.job_position.id,
        job_application_id=app_note1.job_application.id,
    )


@pytest.fixture
def app_note1_context_with_id(db, app_note1):

    return JobApplicationChildContext(
        id=app_note1.id,
        workspace_id=app_note1.job_application.workspace.workspace_id,
        company_id=app_note1.job_application.job_position.company.id,
        job_position_id=app_note1.job_application.job_position.id,
        job_application_id=app_note1.job_application.id,
    )


# ============================================================================
# Documents
# ============================================================================


from django.core.files.uploadedfile import SimpleUploadedFile
from apps.documents.models import DocumentType, Document


class FakeFile:

    def __init__(self, content, chunk_size: int, name: str = "Doc"):

        self.content = content
        self.chunk_size = chunk_size
        self._name = name
        self._committed = True

    @property
    def name(self):
        return self._name

    def chunks(self):

        for i in range(0, len(self.content), self.chunk_size):
            yield self.content[i:i + self.chunk_size]


@pytest.fixture
def api_upload_file1():

    return SimpleUploadedFile(
        "test1.txt", b"test1", content_type="text/plain"
    )


@pytest.fixture
def api_upload_file2():

    return SimpleUploadedFile(
        "test2.txt", b"test2", content_type="text/plain"
    )


@pytest.fixture
def doc_type1_user1_valid_data():

    return {"name": "Document Type 1", "description": "Description 1"}


@pytest.fixture
def document_type_user1(user1):

    return DocumentType.objects.create(
        owner=user1,
        name="Doc Type 1",
    )


@pytest.fixture
def document_type2_user1(user1):

    return DocumentType.objects.create(
        owner=user1,
        name="Doc Type 2",
    )


@pytest.fixture
def document_type_user2(user2):

    return DocumentType.objects.create(
        owner=user2,
        name="Doc Type 1",
    )


@pytest.fixture
def doc1_user1_valid_data(document_type_user1, fake_file1):

    return {
        "name": "Document 1",
        "document_type": document_type_user1,
        "file": fake_file1
    }


@pytest.fixture
def doc1_user1_api_valid_data(document_type_user1, api_upload_file1):

    return {
        "name": "Document 1",
        "document_type": document_type_user1.id,
        "file": api_upload_file1
    }


@pytest.fixture
def doc1_user1_api_updated_valid_data(document_type2_user1, api_upload_file2):

    return {
        "name": "Document 1 Edited",
        "document_type": document_type2_user1.id,
        "file": api_upload_file2
    }


@pytest.fixture
def doc1_user1(document_type_user1, fake_file1):

    return Document.objects.create(
        name="Document 1",
        owner=document_type_user1.owner,
        document_type=document_type_user1,
        file=fake_file1,
        file_hash="hash_1"
    )


@pytest.fixture
def doc2_user1(document_type2_user1, fake_file2):

    return Document.objects.create(
        name="Document 2",
        owner=document_type2_user1.owner,
        document_type=document_type2_user1,
        file=fake_file2,
        file_hash="hash_2"
    )


@pytest.fixture
def doc1_user2(document_type_user2, fake_file1):

    return Document.objects.create(
        name="Document 1",
        owner=document_type_user2.owner,
        document_type=document_type_user2,
        file=fake_file1,
        file_hash="hash_1"
    )


@pytest.fixture
def fake_file1():

    return SimpleUploadedFile(
        name="Doc.txt",
        content="Some File".encode("utf-8"),
        content_type="text/plain",
    )


@pytest.fixture
def fake_file2():

    return SimpleUploadedFile(
        name="Doc2.txt",
        content="Some File 222".encode("utf-8"),
        content_type="text/plain",
    )


