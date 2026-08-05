from mimetypes import guess_type

from django.http import FileResponse
from django.utils.text import slugify


class DocumentFileResponseMixin:

    as_attachment = False

    def get_document(self):

        return self.get_object()

    def get_response(self):

        document = self.get_document()

        content_type, _ = guess_type(document.file.name)

        return FileResponse(
            document.file.open("rb"),
            as_attachment=self.as_attachment,
            filename=slugify(document.name),
            content_type=content_type,
        )
