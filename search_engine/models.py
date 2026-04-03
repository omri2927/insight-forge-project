"""Models for storing search history and cached search results."""

from django.db import models
from django.contrib.auth.models import User
from documents.models import Document


class SearchQuery(models.Model):
    # Persist the user and the raw query used for a search operation.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')

    query_text = models.TextField(blank=True, null=True)
    # Flexible JSON filters allow future search options without schema changes.
    filters_json = models.JSONField(default=dict, blank=True, null=True)

    results_count = models.IntegerField(blank=True, null=True)
    executed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"query sent by {self.user.username} - {self.query_text if self.query_text else ''}"

    class Meta:
        # Keep the newest queries first.
        ordering = ['-executed_at', 'results_count']


class SearchResultCache(models.Model):
    # Each cached result belongs to one executed search query.
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE,
        related_name="cache_entries")

    # Cached search results point back to the matched document.
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="search_results"
    )

    snippet = models.TextField(blank=True, null=True)
    score = models.FloatField(default=0.0)
    matched_count = models.PositiveIntegerField(blank=True, null=True)

    # Timestamp showing when the cache entry was created.
    cached_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = self.snippet[:30] if self.snippet else ''
        return f"results: snippet - {preview}, score - {self.score}"
