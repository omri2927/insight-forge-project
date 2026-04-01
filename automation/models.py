from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class AutomationJob(models.Model):
    class AutomationTasks(models.TextChoices):
        PROCESSING_TASK = 'PROCESSING_TASK', 'processing'
        ANALYTICS_TASK = 'ANALYTICS_TASK', 'analytics'
        MAINTENANCE_TASK = 'MAINTENANCE_TASK', 'maintenance'
        INDEXING_TASK = 'INDEXING_TASK', 'indexing'

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='automation_jobs')
    name = models.CharField(max_length=50)

    job_type = models.CharField(
        max_length=30,
        choices=AutomationTasks.choices,
        default=AutomationTasks.MAINTENANCE_TASK)

    target_document = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='automations'
    )

    trigger_config_json = models.JSONField(default=dict, blank=True, null=True)
    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AutomationRun(models.Model):
    job = models.ForeignKey(
        AutomationJob,
        on_delete=models.CASCADE,
        related_name='runs'
    )
    status = models.CharField(max_length=50, blank=True, null=True)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    result_summary = models.TextField(blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)


class SystemLog(models.Model):
    class TextLevels(models.TextChoices):
        INFO = 'INFO', 'info'
        WARNING = 'WARNING', 'warning'
        ERROR = 'ERROR', 'error'
        DEBUG = 'DEBUG', 'debug'

    level = models.CharField(
        max_length=30,
        choices=TextLevels.choices,
        default=TextLevels.INFO
    )
    source = models.CharField(max_length=100)
    message = models.TextField()

    context_json = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)