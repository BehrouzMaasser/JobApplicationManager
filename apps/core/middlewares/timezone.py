from django.utils import timezone
from zoneinfo import ZoneInfo


class TimezoneMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        tz = "UTC"

        user = getattr(request, "user", None)

        if user and user.is_authenticated:

            tz = getattr(user, "timezone", "UTC")

        timezone.activate(ZoneInfo(tz))

        response = self.get_response(request)

        timezone.deactivate()

        return response
