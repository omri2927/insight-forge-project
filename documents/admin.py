"""Admin configuration for document-related models."""

from django.contrib import admin
from .models import DocumentType, Document, DocumentProcessingResult


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    # Basic lookup fields for document type records.
    list_display = ('name', 'extension', 'mime_type', 'is_structured')
    search_fields = ('name', 'extension')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # Show document ownership, metadata, and processing status at a glance.
    list_display = ('get_owner', 'title', 'original_file_name', 'get_type',
                    'file_size', 'upload_status', 'is_active', 'updated_at')
    list_filter = ('upload_status', 'is_active', 'uploaded_at')
    search_fields = ('title', 'owner__username', 'original_file_name', 'document_type__name', 'checksum')
    # These fields are populated by the system and should not be edited manually.
    readonly_fields = ('upload_status', 'checksum', 'uploaded_at', 'updated_at')

    def get_owner(self, obj):
        # Resolve the username from the related owner record.
        return obj.owner.username
    get_owner.short_description = 'Owner'

    def get_type(self, obj):
        # Gracefully handle documents that do not have a type assigned yet.
        return obj.document_type.name if obj.document_type else "-"
    get_type.short_description = 'Document Type'


@admin.register(DocumentProcessingResult)
class DocumentProcessingResultAdmin(admin.ModelAdmin):
    # Expose the main parsing and indexing outcomes for each processed file.
    list_display = ('get_document', 'parsing_status', 'indexing_status',
                    'row_count', 'column_count', 'processed_at')
    list_filter = ('parsing_status', 'indexing_status', 'processed_at')
    readonly_fields = ('parsing_status', 'indexing_status', 'processed_at')

    def get_document(self, obj):
        return obj.document.title
    get_document.short_description = 'Document'
