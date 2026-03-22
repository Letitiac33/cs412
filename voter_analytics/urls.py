# File: urls.py
# Author: Letitia Caspersen (letitiac@bu.edu), 3/22/2026
# Description: URL patterns for the voter_analytics app

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.GraphsListView.as_view(), name='graphs'),
]
