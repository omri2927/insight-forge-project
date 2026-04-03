"""Admin configuration for analytics models."""

from django.contrib import admin
from .models import AnalyticsReport, ChartArtifact


@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    # Make reports easy to scan by owner, source document, and type.
    list_display = ('get_owner', 'name', 'get_document', 'report_type', 'updated_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('name', 'report_type')
    # Generated content and timestamps should not be edited manually.
    readonly_fields = ('summary_text', 'created_at', 'updated_at')

    def get_owner(self, obj):
        # Show the username for the related owner record.
        return obj.owner.username
    get_owner.short_description = 'Owner'

    def get_document(self, obj):
        # Show the linked document title in the report list view.
        return obj.document.title
    get_document.short_description = 'Document'


@admin.register(ChartArtifact)
class ChartArtifactAdmin(admin.ModelAdmin):
    # Display the chart metadata most useful for admins.
    list_display = ('get_report', 'title', 'chart_type', 'created_at')
    list_filter = ('chart_type', 'created_at')
    readonly_fields = ('created_at',)

    def get_report(self, obj):
        # Resolve the report name from the foreign key relation.
        return obj.report.name
    get_report.short_description = 'Report'
