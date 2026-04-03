from django.contrib import admin
from .models import AutomationJob, AutomationRun, SystemLog

# Register your models here.
@admin.register(AutomationJob)
class AutomationJobAdmin(admin.ModelAdmin):
    list_display = ('get_owner', 'name', 'job_type', 'get_target_document', 'is_enabled', 'updated_at')
    list_filter = ('job_type', 'is_enabled', 'created_at')
    search_fields = ('owner__username', 'name', 'job_type', 'target_document__title')
    readonly_fields = ('created_at', 'updated_at')

    def get_owner(self, obj):
        return obj.owner.username
    get_owner.short_description = 'Owner'

    def get_target_document(self, obj):
        return obj.target_document.title if obj.target_document else '-'
    get_target_document.short_description = 'Target Document'

@admin.register(AutomationRun)
class AutomationRunAdmin(admin.ModelAdmin):
    list_display = ('get_job', 'status', 'started_at', 'finished_at')
    list_filter = ('status', 'started_at', 'finished_at')
    readonly_fields = ('status', 'started_at', 'finished_at', 'result_summary', 'error_message')

    def get_job(self, obj):
        return obj.job.name
    get_job.short_description = 'Job'

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('level', 'source', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('level', 'source', 'message')
    readonly_fields = ('created_at',)