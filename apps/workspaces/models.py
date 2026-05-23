import uuid

from django.db import models
from django.conf import settings


# Create your models here.


class Workspace(models.Model):

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
                fields=["owner", "name"], name="unique_workspace_name_per_user"
            )
        ]
        indexes = [
            models.Index(fields=["owner", "name"]),
        ]

    def __str__(self):

        return f"{self.name} ({self.owner.email})"
