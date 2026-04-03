"""Admin configuration for search history and cached search results."""

from django.contrib import admin
from .models import SearchQuery, SearchResultCache


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    # Show who searched, what they searched for, and when.
    list_display = ('get_user', 'query_text', 'results_count', 'executed_at')
    list_filter = ('executed_at',)
    search_fields = ('user__username', 'query_text')
    readonly_fields = ('results_count', 'executed_at')

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'


@admin.register(SearchResultCache)
class SearchResultCacheAdmin(admin.ModelAdmin):
    # Show which cached result belongs to which query and document.
    list_display = ('get_search_query', 'get_document', 'snippet', 'score', 'matched_count', 'cached_at')
    list_filter = ('cached_at',)
    readonly_fields = ('snippet', 'score', 'matched_count', 'cached_at')

    def get_search_query(self, obj):
        return obj.search_query.query_text
    get_search_query.short_description = 'Search Query'

    def get_document(self, obj):
        return obj.document.title
    get_document.short_description = 'Document'
