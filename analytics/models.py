from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class AnalyticsReport(models.Model):
    class ReportTypes(models.TextChoices):
        SUMMARY = 'SUMMARY', 'Summary'
        PII_DETECTION = 'PII_DETECTION', 'PII Detection'
        DATA_EXTRACTION = 'DATA_EXTRACTION', 'Data Extraction'
        SENTIMENT = 'SENTIMENT', 'Sentiment Analysis'
        COMPLIANCE = 'COMPLIANCE', 'Compliance Check'

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reports')

    name = models.CharField(max_length=50)
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="analytics"
    )

    report_type = models.CharField(
        max_length=50,
        choices=ReportTypes.choices,
        default=ReportTypes.SUMMARY
    )
    parameters_json = models.JSONField(default=dict, blank=True, null=True)
    summary_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"report data: name - {self.name}, type - {self.report_type}"

    class Meta:
        ordering = ['-created_at', '-updated_at', 'name']


class ChartArtifact(models.Model):
    class ChartType(models.TextChoices):
        BAR_CHART = 'BAR_CHART', 'bar chart'
        LINE_CHART = 'LINE_CHART', 'line chart'
        PIE_CHART = 'PIE_CHART', 'pie chart'
        SCATTER_CHART = 'SCATTER_CHART', 'scatter chart'
        HISTOGRAM_CHART = 'HISTOGRAM_CHART', 'histogram chart'
        AREA_CHART = 'AREA_CHART', 'area chart'
        BUBBLE_CHART = 'BUBBLE_CHART', 'bubble chart'
        CANDLESTICK_CHART = 'CANDLESTICK_CHART', 'candlestick chart'

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

    image_path = models.ImageField(upload_to='charts/%Y/%m/%d/', blank=True, null=True)
    config_json = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title: {self.title}, chart type: {self.chart_type}"

