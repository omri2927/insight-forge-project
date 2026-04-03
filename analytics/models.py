"""Models for generated analytics reports and chart outputs."""

from django.db import models
from django.contrib.auth.models import User
from documents.models import Document


class AnalyticsReport(models.Model):
    class ReportTypes(models.TextChoices):
        # Predefined report categories supported by the analytics pipeline.
        SUMMARY = 'SUMMARY', 'Summary'
        PII_DETECTION = 'PII_DETECTION', 'PII Detection'
        DATA_EXTRACTION = 'DATA_EXTRACTION', 'Data Extraction'
        SENTIMENT = 'SENTIMENT', 'Sentiment Analysis'
        COMPLIANCE = 'COMPLIANCE', 'Compliance Check'

    # The user who requested or owns the generated report.
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports')

    name = models.CharField(max_length=50)
    # Each report is attached to a single source document.
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="analytics"
    )

    # Persist the report category together with flexible parameters and output text.
    report_type = models.CharField(
        max_length=50,
        choices=ReportTypes.choices,
        default=ReportTypes.SUMMARY
    )
    parameters_json = models.JSONField(default=dict, blank=True, null=True)
    summary_text = models.TextField(blank=True, null=True)

    # Automatic timestamps for sorting and auditing.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Human-readable identifier for Django admin and debugging.
        return f"report data: name - {self.name}, type - {self.report_type}"

    class Meta:
        # Show the newest reports first.
        ordering = ['-created_at', '-updated_at', 'name']


class ChartArtifact(models.Model):
    class ChartType(models.TextChoices):
        # Supported visualization types for report outputs.
        BAR_CHART = 'BAR_CHART', 'bar chart'
        LINE_CHART = 'LINE_CHART', 'line chart'
        PIE_CHART = 'PIE_CHART', 'pie chart'
        SCATTER_CHART = 'SCATTER_CHART', 'scatter chart'
        HISTOGRAM_CHART = 'HISTOGRAM_CHART', 'histogram chart'
        AREA_CHART = 'AREA_CHART', 'area chart'
        BUBBLE_CHART = 'BUBBLE_CHART', 'bubble chart'
        CANDLESTICK_CHART = 'CANDLESTICK_CHART', 'candlestick chart'

    # Each chart belongs to a single analytics report.
    report = models.ForeignKey(
        AnalyticsReport,
        on_delete=models.CASCADE,
        related_name='charts')
    title = models.CharField(max_length=50)

    chart_type = models.CharField(
        max_length=25,
        choices=ChartType.choices,
        default=ChartType.LINE_CHART
    )

    # Store the rendered image and the chart configuration used to build it.
    image_path = models.ImageField(upload_to='charts/%Y/%m/%d/', blank=True, null=True)
    config_json = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title: {self.title}, chart type: {self.chart_type}"
