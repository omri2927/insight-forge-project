"""Models for uploaded documents and their processing results."""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def document_upload_path(instance, filename):
    # Organize uploads by owner and by year/month for easier storage management.
    upload_date = instance.uploaded_at or timezone.now()
    return f'documents/user_{instance.owner.id}/{upload_date:%Y/%m}/{filename}'


class DocumentType(models.Model):
    # High-level metadata describing a supported file type.
    name = models.CharField(max_length=50, unique=True)
    extension = models.CharField(max_length=30, blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)

    is_structured = models.BooleanField(default=False)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.extension if self.extension else ''}"


class Document(models.Model):
    class UploadStatus(models.TextChoices):
        # Track the lifecycle of the upload pipeline.
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    # Core ownership and storage fields for an uploaded file.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=75, blank=True, null=True)
    original_file_name = models.CharField(max_length=150, blank=True, null=True)
    stored_file = models.FileField(upload_to=document_upload_path)

    # Optional classification metadata for the file.
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )
    file_size = models.BigIntegerField(blank=True, null=True)
    # The checksum helps with deduplication and integrity checks.
    checksum = models.CharField(max_length=64, editable=False, null=True, db_index=True)

    upload_status = models.CharField(
        max_length=25,
        choices=UploadStatus.choices,
        default=UploadStatus.PENDING,
        db_index=True)
    is_active = models.BooleanField(default=True)

    # Timestamps support sorting and audit history.
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title if self.title else ''} - ext: {self.document_type}"

    class Meta:
        ordering = ['-uploaded_at', '-updated_at', 'file_size']


class DocumentProcessingResult(models.Model):
    class ParsingStatus(models.TextChoices):
        # Parsing status focuses on reading and understanding the raw file.
        PENDING = 'PENDING', 'pending'
        STARTING = 'STARTING', 'starting'
        SUCCESS = 'SUCCESS', 'success'
        FAILED = 'FAILED', 'failed'
        UNSUPPORTED_FORMAT = 'UNSUPPORTED_FORMAT', 'unsupported format'

    class IndexingStatus(models.TextChoices):
        # Indexing status focuses on search/index pipeline progress.
        WAITING = 'WAITING', 'waiting'
        INDEXING = 'INDEXING', 'indexing'
        SUCCESS = 'SUCCESS', 'success'
        PARTIAL = 'PARTIAL', 'partial'
        FAILED = 'FAILED', 'failed'

    # One processing result record per document.
    document = models.OneToOneField(
        Document,
        on_delete=models.CASCADE,
        related_name='processing_result')

    parsing_status = models.CharField(
        max_length=50,
        choices=ParsingStatus.choices,
        default=ParsingStatus.PENDING
    )
    indexing_status = models.CharField(
        max_length=50,
        choices=IndexingStatus.choices,
        default=IndexingStatus.WAITING
    )

    # Optional structural metadata captured during processing.
    row_count = models.IntegerField(blank=True, null=True)
    column_count = models.IntegerField(blank=True, null=True)

    detected_encoding = models.CharField(max_length=30, blank=True, null=True)
    detected_language = models.CharField(max_length=30, blank=True, null=True)

    summary = models.TextField(blank=True, null=True)
    processed_at = models.DateTimeField(auto_now_add=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"results: {self.row_count} rows, {self.column_count} columns"

    class Meta:
        ordering = ['-processed_at', 'row_count', 'column_count']
