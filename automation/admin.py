"""Admin configuration for automation and system logging models."""

from django.contrib import admin
from .models import AutomationJob, AutomationRun, SystemLog


@admin.register(AutomationJob)
class AutomationJobAdmin(admin.ModelAdmin):
    # Expose key scheduling fields for quick monitoring in Django admin.
    list_display = ('get_owner', 'name', 'job_type', 'get_target_document', 'is_enabled', 'updated_at')
    list_filter = ('job_type', 'is_enabled', 'created_at')
    search_fields = ('owner__username', 'name', 'job_type', 'target_document__title')
    readonly_fields = ('created_at', 'updated_at')

    def get_owner(self, obj):
        # Show the owning username instead of the raw relation object.
        return obj.owner.username
    get_owner.short_description = 'Owner'

    def get_target_document(self, obj):
        # Some jobs are not tied to a document, so fall back to a dash.
        return obj.target_document.title if obj.target_document else '-'
    get_target_document.short_description = 'Target Document'


@admin.register(AutomationRun)
class AutomationRunAdmin(admin.ModelAdmin):
    # Surface execution state and timing for each run.
    list_display = ('get_job', 'status', 'started_at', 'finished_at')
    list_filter = ('status', 'started_at', 'finished_at')
    readonly_fields = ('status', 'started_at', 'finished_at', 'result_summary', 'error_message')

    def get_job(self, obj):
        return obj.job.name
    get_job.short_description = 'Job'


@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    # Keep the system log searchable by source, level, and message text.
    list_display = ('level', 'source', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('level', 'source', 'message')
    readonly_fields = ('created_at',)
