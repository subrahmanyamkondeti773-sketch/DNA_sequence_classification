"""
Root URL configuration for DNA Classification Project.
"""
from django.contrib import admin
from django.urls import path, include
from dna_classifier import api_views
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "DNA Team Administration"
admin.site.site_title = "DNA Team Admin Portal"
admin.site.index_title = "Welcome to DNA Team Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dna_classifier.urls')),
    path('users/', include('users.urls')),
    
    # Mobile API Endpoints
    path('api/register/', api_views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', api_views.LoginAPIView.as_view(), name='api_login'),
    path('api/stats/', api_views.DashboardStatsAPIView.as_view(), name='api_stats'),
    path('api/classify/', api_views.ClassifyDNAAPIView.as_view(), name='api_classify'),
    path('api/history/', api_views.PredictionHistoryAPIView.as_view(), name='api_history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
