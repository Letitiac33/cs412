# File: urls.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/3/2026
# Description: URL patterns for Sealy's restaurant app

from django.urls import path                                                                                                          
from . import views                                                                                                                   
                                                                                                                                        
urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]                                                                                                                                     
     