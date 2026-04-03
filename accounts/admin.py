from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'display_name', 'role', 'company_name', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'display_name', 'role', 'company_name')
    readonly_fields = ('created_at', 'updated_at')

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'