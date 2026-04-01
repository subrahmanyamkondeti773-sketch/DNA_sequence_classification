"""
DNA Classifier URL configuration.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dna/classify/', views.dna_input_view, name='dna_input'),
    path('dna/result/<int:pk>/', views.result_view, name='result'),
    path('dna/history/', views.history_view, name='history'),
    path('dna/history/<int:pk>/', views.history_detail_view, name='history_detail'),
    path('dna/export/<int:pk>/', views.export_pdf_view, name='export_pdf'),
    path('api/analytics/', views.analytics_api_view, name='analytics_api'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('dna/accuracy-report/', views.model_accuracy_view, name='model_accuracy'),
]
