from django.db import models

from apps.accounts.models import User


class DummyTag(models.Model):
    """
    Test model used for BaseService contract testing.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="test_tags",
    )

    name = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return self.name


class DummyItem(models.Model):
    """
    Test aggregate used for BaseService contract testing.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="test_items",
    )

    name = models.CharField(
        max_length=100,
    )

    tags = models.ManyToManyField(
        DummyTag,
        related_name="items",
    )

    def __str__(self):
        return self.name
