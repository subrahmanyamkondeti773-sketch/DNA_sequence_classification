"""
Root URL configuration for DNA Classification Project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "DNA Classification Admin"
admin.site.site_title = "DNA Admin Portal"
admin.site.index_title = "Welcome to DNA Classification Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dna_classifier.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
