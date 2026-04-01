"""
Users app models - Extended User Profile.
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended profile linked to Django's built-in User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    team_name = models.CharField(max_length=100, blank=True, default='', help_text="Identify your team (e.g., Team Alpha)")
    bio = models.TextField(max_length=500, blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def total_predictions(self):
        return self.user.dnasequence_set.count()

    @property
    def recent_prediction(self):
        return self.user.dnasequence_set.first()
