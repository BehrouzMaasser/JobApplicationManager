import hashlib
import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.db.models.functions import Lower
from django.utils.text import slugify


# Helper functions

def document_upload_path(instance, filename):
    """

    :param instance: Document instance
    :param filename: Document file name
    :return:
        media/docs/<owner-document-directory>/<document-type>/<unique-filename>
    """
    document_type = slugify(instance.document_type.name)
    file_name_extension = filename.split('.')
    if len(file_name_extension) != 2:
        raise ValidationError({
            "file_name": "File should not have '.' in its name!"
        })
    unique_name = f"{uuid.uuid4()}.{file_name_extension[1]}"

    return os.path.join(
        "docs",
        str(instance.owner.documents_directory),
        document_type,
        unique_name
    )


def calculate_file_hash(file_obj):

    sha256 = hashlib.sha256()

    for chunk in file_obj.chunks():
        sha256.update(chunk)

    return sha256.hexdigest()


# Create your models here.


class DocumentType(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="document_types",
    )
    name = models.CharField(max_length=40)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "owner"]
        constraints = [
            models.UniqueConstraint(
                "owner", Lower("name"), name="unique_document_type_per_user"
            )
        ]

    def __str__(self):

        return f"{self.name} {self.owner}"

    def save(self, *args, **kwargs):

        if not self.description:
            self.description = None

        super().save(*args, **kwargs)


class Document(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(upload_to=document_upload_path)
    file_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        ordering = ["owner", "name", "created_at", "updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"], name="unique_document_name_per_user"
            )
        ]
        indexes = [
            models.Index(fields=["owner", "name"]),
        ]

    def __str__(self):

        return f"{self.name} {self.owner}"

    def clean(self):

        if [self.owner_id, self.document_type_id, self.file.name].count(None):
            return
        if self.owner_id != self.document_type.owner_id:
            raise ValidationError(
                {
                    "owner": [
                        "Owner of the document and document type should be the same"
                    ],
                    "document_type": [
                        "Owner of the document and document type should be the same"
                    ],
                }
            )

    def save(self, *args, **kwargs):

        if not self.file_hash:
            self.file_hash = calculate_file_hash(self.file)

            # Check if identical file already exists for this user
            existing_file_hash = Document.objects.filter(
                owner=self.owner,
                file_hash=self.file_hash
            ).first()

            if existing_file_hash:
                # Reuse existing file instead of saving new one
                self.file = existing_file_hash.file
                self.file_hash = existing_file_hash.file_hash

        super().save(*args, **kwargs)
