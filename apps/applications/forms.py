from django import forms

from apps.applications.models import JobApplication, JobApplicationNote


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = [
            "owner",
            "workspace",
            "job_position",
            "status",
            "emails",
            "date_applied",
            "documents"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].empty_label = None
        self.fields["workspace"].empty_label = None
        self.fields["job_position"].empty_label = None
        self.fields["status"].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        emails = cleaned_data.get("emails")
        job_position = cleaned_data.get("job_position")
        if emails and job_position:
            wrong_emails_count = sum([
                1 for email in emails if email.company != job_position.company])
            if wrong_emails_count:
                self.add_error("emails",f"Emails should belong to the "
                                        f"job position's company! Number of wrong"
                                        f" emails: {wrong_emails_count}")
        return cleaned_data


class JobApplicationNoteForm(forms.ModelForm):
    class Meta:
        model = JobApplicationNote
        fields = [
            "job_application", "title", "content"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["job_application"].empty_label = None
