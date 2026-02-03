# File: urls.py
# Author: Letitia Caspersen (letitiac@bu.edu), 1/28/2026
# Description: URL patterns for Sealy's restaurant app

from django.urls import path                                                                                                          
from . import views                                                                                                                   
                                                                                                                                        
urlpatterns = [       
    path('', views.restaurant, name='main'), 
    path('main/', views.restaurant, name='main'), 
    path('order/', views.restaurant, name='order'),
    path('confirmation/', views.restaurant, name='confirmation'),                                                                                                                                                                                     
]                                                                                                                                     
     