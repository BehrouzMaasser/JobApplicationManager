from django.contrib import admin
from .models import Workspace

# Register your models here.


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at", "updated_at")
    search_fields = ("name", "owner__email", "owner__last_name")
    list_filter = ("created_at", "owner__email", "owner__last_name")
