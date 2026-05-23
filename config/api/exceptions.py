from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is None:
        return response

    return Response(
        {
            "error": {
                "code": "api_error",
                "message": str(exc),
                "details": response.data,
            }
        },
        status=response.status_code,
    )
