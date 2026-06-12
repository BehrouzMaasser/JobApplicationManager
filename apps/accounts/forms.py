from zoneinfo import available_timezones

from django import forms
from apps.accounts.models import User


class UserSettingsForm(forms.ModelForm):

    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in sorted(available_timezones())],
    )

    class Meta:

        model = User
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "timezone",
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # ensure current value is always correctly bound
        if self.instance and self.instance.pk:
            self.fields["timezone"].initial = self.instance.timezone
