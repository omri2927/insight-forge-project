from django.db import models
from django.contrib.auth.models import User
from documents.models import Document

class SearchQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')

    query_text = models.TextField(blank=True, null=True)
    filters_json = models.JSONField(default=dict, blank=True, null=True)

    results_count = models.IntegerField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"query sent by {self.user.username} - {self.query_text if self.query_text else ''}"

    class Meta:
        ordering = ['-executed_at', 'results_count']


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

    def __str__(self):
        return f"results: snippet - {self.snippet[:30] if self.snippet else ''}, score - {self.score}"