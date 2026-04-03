"""Data models for user profile information."""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    # Link each profile to exactly one Django auth user.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Optional business/profile metadata shown in the product UI and admin.
    display_name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)

    # Automatic audit timestamps.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Fall back to the username when a custom display name is not available.
        return f"{self.display_name or self.user.username} - ({self.role or 'No Role'})"
