"""
Database models for the documents application.

This module defines document types and uploaded documents, along with helper
functions for generating upload paths and calculating file hashes.
"""

import hashlib
import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify


# =========================================================
# Helper functions
# =========================================================

def document_upload_path(instance, filename):
    """
    Generate the upload path for a document file.

    Files are stored using the following structure::

        docs/<owner-document-directory>/<document-type>/<unique-filename>

    Args:
        instance:
            The document instance being saved.

        filename:
            Original uploaded filename.

    Returns:
        The relative upload path for the file.

    Raises:
        ValidationError:
            If the filename contains more than one period.
    """

    document_type = slugify(instance.document_type.name)

    file_name_extension = filename.split(".")

    if len(file_name_extension) != 2:
        raise ValidationError(
            {
                "file_name": "File should not have '.' in its name!"
            }
        )

    unique_name = f"{uuid.uuid4()}.{file_name_extension[1]}"

    return os.path.join(
        "docs",
        str(instance.owner.documents_directory),
        document_type,
        unique_name,
    )


def calculate_file_hash(file_obj):
    """
    Calculate the SHA-256 hash of an uploaded file.

    Args:
        file_obj:
            Uploaded file object.

    Returns:
        Hexadecimal SHA-256 digest.
    """

    sha256 = hashlib.sha256()

    for chunk in file_obj.chunks():
        sha256.update(chunk)

    return sha256.hexdigest()


# =========================================================
# Models
# =========================================================

class DocumentType(models.Model):
    """
    Represents a user-defined category used to organize documents.
    """

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
        """Model metadata."""

        ordering = ("name", "owner")

        constraints = [
            models.UniqueConstraint(
                "owner",
                Lower("name"),
                name="unique_document_type_per_user",
                violation_error_code="duplicate_type_document_name",
                violation_error_message="A document type with this name already "
                                        "exists.",
            )
        ]

    def __str__(self):
        """Return the document type name."""

        return self.name

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if not self.description:
            self.description = None

        super().save(*args, **kwargs)


class Document(models.Model):
    """
    Represents an uploaded document owned by a user.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    file = models.FileField(upload_to=document_upload_path)
    file_hash = models.CharField(max_length=64, editable=False)

    class Meta:
        """Model metadata."""

        ordering = (
            "owner",
            "name",
            "created_at",
            "updated_at",
        )

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_document_name_per_user",
                violation_error_code="duplicate_document_name",
                violation_error_message="A document with this name already exists.",
            )
        ]

        indexes = [
            models.Index(fields=["owner", "name"]),
        ]

    def __str__(self):
        """Return the document name."""

        return self.name

    def clean(self):
        """
        Validate ownership consistency between the document and its type.
        """

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
        """
        Calculate the file hash and reuse an existing stored file when an
        identical file has already been uploaded by the same user.
        """

        if not self.file_hash:
            self.file_hash = calculate_file_hash(self.file)

            existing_file = Document.objects.filter(
                owner=self.owner,
                file_hash=self.file_hash,
            ).first()

            if existing_file:
                self.file = existing_file.file
                self.file_hash = existing_file.file_hash

        super().save(*args, **kwargs)