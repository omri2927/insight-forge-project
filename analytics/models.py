from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class AnalyticsReport(models.Model):
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

    report_type = models.CharField(max_length=50, blank=True, null=True)
    parameters_json = models.JSONField(default=dict, blank=True, null=True)
    summary_text = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


