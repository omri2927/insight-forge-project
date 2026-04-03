"""Models that represent automation jobs, runs, and system logs."""

from django.db import models
from django.contrib.auth.models import User
from documents.models import Document


class AutomationJob(models.Model):
    class AutomationTasks(models.TextChoices):
        # High-level task categories supported by the automation system.
        PROCESSING_TASK = 'PROCESSING_TASK', 'processing'
        ANALYTICS_TASK = 'ANALYTICS_TASK', 'analytics'
        MAINTENANCE_TASK = 'MAINTENANCE_TASK', 'maintenance'
        INDEXING_TASK = 'INDEXING_TASK', 'indexing'

    # The user who owns or created the automation job.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='automation_jobs')
    name = models.CharField(max_length=50)

    # Store the job category so workers can route execution logic.
    job_type = models.CharField(
        max_length=30,
        choices=AutomationTasks.choices,
        default=AutomationTasks.MAINTENANCE_TASK
    )

    # A job can optionally target a specific document.
    target_document = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='automations'
    )

    # JSON configuration keeps trigger rules flexible without extra tables.
    trigger_config_json = models.JSONField(default=dict, blank=True, null=True)
    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"job type: {self.job_type}, target document: {self.target_document}"


class AutomationRun(models.Model):
    class Status(models.TextChoices):
        # Track the lifecycle of an execution attempt.
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        TIMEOUT = 'TIMEOUT', 'Timeout'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # Each run belongs to one automation job.
    job = models.ForeignKey(
        AutomationJob,
        on_delete=models.CASCADE,
        related_name='runs'
    )
    status = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    # Capture both the start time and the optional finish time of the run.
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    # Store a short result and an optional failure message for diagnostics.
    result_summary = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"status: {self.status if self.status else ''}"

    class Meta:
        # Newer executions should appear first in admin and query results.
        ordering = ['-started_at', '-finished_at', 'job__name']


class SystemLog(models.Model):
    class TextLevels(models.TextChoices):
        # Standard log severity levels.
        INFO = 'INFO', 'info'
        WARNING = 'WARNING', 'warning'
        ERROR = 'ERROR', 'error'
        DEBUG = 'DEBUG', 'debug'

    level = models.CharField(
        max_length=30,
        choices=TextLevels.choices,
        default=TextLevels.INFO,
        db_index=True
    )
    source = models.CharField(max_length=100)
    message = models.TextField()

    # Extra structured context can be stored alongside a log entry.
    context_json = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"level: {self.level}, source: {self.source}"

    class Meta:
        ordering = ['-created_at', 'source']
