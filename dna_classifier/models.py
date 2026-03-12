"""
DNA Classifier app models.
"""
from django.db import models
from django.contrib.auth.models import User


class DNASequence(models.Model):
    """Stores each DNA classification prediction with AI explanation."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dnasequence_set')
    sequence = models.TextField(help_text="The cleaned DNA sequence (ATGC only)")
    prediction = models.CharField(max_length=200)
    confidence_score = models.FloatField(default=0.0, help_text="Prediction confidence (0-1)")
    ai_explanation = models.TextField(blank=True, default='')
    ai_suggestions = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'DNA Sequence'
        verbose_name_plural = 'DNA Sequences'

    def __str__(self):
        return f"{self.user.username} - {self.prediction} ({self.created_at.strftime('%Y-%m-%d')})"

    @property
    def short_sequence(self):
        """Returns first 60 characters of sequence for display."""
        return self.sequence[:60] + '...' if len(self.sequence) > 60 else self.sequence

    @property
    def confidence_percent(self):
        """Returns confidence as percentage string."""
        return f"{self.confidence_score * 100:.1f}%"

    @property
    def confidence_color(self):
        """Returns Bootstrap color class based on confidence."""
        if self.confidence_score >= 0.8:
            return 'success'
        elif self.confidence_score >= 0.5:
            return 'warning'
        return 'danger'


class APILog(models.Model):
    """Logs all API calls for monitoring."""
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
    ]

    endpoint = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    response_time = models.FloatField(default=0.0, help_text="Response time in seconds")
    error_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'

    def __str__(self):
        return f"{self.endpoint} - {self.status} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
