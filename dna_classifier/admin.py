"""
DNA Classifier admin registration.
Custom admin with list filters, search, and display fields.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import DNASequence, APILog


@admin.register(DNASequence)
class DNASequenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'short_sequence_display', 'prediction',
                    'confidence_display', 'created_at']
    list_filter = ['prediction', 'created_at', 'user']
    search_fields = ['user__username', 'sequence', 'prediction']
    readonly_fields = ['created_at', 'confidence_score']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25

    @admin.display(description='Sequence (preview)')
    def short_sequence_display(self, obj):
        seq = obj.sequence[:50] + '...' if len(obj.sequence) > 50 else obj.sequence
        return format_html('<code style="font-size:11px">{}</code>', seq)

    @admin.display(description='Confidence')
    def confidence_display(self, obj):
        pct = obj.confidence_score * 100
        color = '#22c55e' if pct >= 80 else '#f59e0b' if pct >= 50 else '#ef4444'
        return format_html(
            '<span style="color:{}; font-weight:bold;">{:.1f}%</span>', color, pct
        )


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ['endpoint', 'status', 'response_time', 'created_at']
    list_filter = ['status', 'endpoint', 'created_at']
    readonly_fields = ['endpoint', 'status', 'response_time', 'error_message', 'created_at']
    ordering = ['-created_at']
    list_per_page = 50
