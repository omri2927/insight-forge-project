from django.contrib import admin
from .models import AnalyticsReport, ChartArtifact

# Register your models here.
@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ('get_owner', 'name', 'get_document', 'report_type', 'updated_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('name', 'report_type')
    readonly_fields = ('summary_text', 'created_at', 'updated_at')

    def get_owner(self, obj):
        return obj.owner.username
    get_owner.short_description = 'Owner'

    def get_document(self, obj):
        return obj.document.title
    get_document.short_description = 'Document'

@admin.register(ChartArtifact)
class ChartArtifactAdmin(admin.ModelAdmin):
    list_display = ('get_report', 'title', 'chart_type', 'created_at')
    list_filter = ('chart_type', 'created_at')
    readonly_fields = ('created_at',)

    def get_report(self, obj):
        return obj.report.name
    get_report.short_description = 'Report'
