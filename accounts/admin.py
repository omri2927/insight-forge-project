"""Admin configuration for the accounts app."""

from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # Show the most useful identity/profile fields in the admin list view.
    list_display = ('get_user', 'display_name', 'role', 'company_name', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'display_name', 'role', 'company_name')
    # Audit timestamps should be read-only in the admin panel.
    readonly_fields = ('created_at', 'updated_at')

    def get_user(self, obj):
        # Display the related Django auth username instead of the raw foreign key.
        return obj.user.username
    get_user.short_description = 'User'
