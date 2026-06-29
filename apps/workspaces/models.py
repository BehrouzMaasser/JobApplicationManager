"""
Workspace domain models.

A workspace represents an isolated environment owned by a single user.
All companies, job positions, applications and related resources belong to
a workspace.
"""

import uuid

from django.db import models
from django.conf import settings


class Workspace(models.Model):
    """
    Represents a user's workspace.

    A workspace acts as the top-level container for all job tracking resources and
     isolates one user's data from another's.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="workspaces"
    )

    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    workspace_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)

    class Meta:

        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_workspace_name_per_user",
                violation_error_message="A workspace already exists with this name",
                violation_error_code="duplicate_workspace_name",
            )
        ]
        indexes = [
            models.Index(fields=["owner", "name"]),
        ]

    def __str__(self):

        return f"{self.name} ({self.owner.email})"
