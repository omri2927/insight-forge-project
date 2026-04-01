from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')

    query_text = models.TextField(blank=True, null=True)
    filters_json = models.JSONField(default=dict, blank=True, null=True)

    results_count = models.IntegerField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)


class SearchResultCache(models.Model):
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE,
        related_name="cache_entries")

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="search_results"
    )

    snippet = models.TextField(blank=True, null=True)
    score = models.FloatField(default=0.0)
    matched_count = models.PositiveIntegerField(blank=True, null=True)

    cached_at = models.DateTimeField(auto_now_add=True)