from django.contrib import admin
from .models import Document, DocumentType


# Register your models here.


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "name", "owner", "document_type", "document_type", "file", "file_hash",
        "created_at", "updated_at"
    )
    search_fields = ("name", )
    list_filter = ("created_at", )


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "description", "created_at")
    search_fields = ("name", )
