# File: urls.py
# Author: Letitia Caspersen (letitiac@bu.edu), 1/28/2026
# Description: URL patterns for Oscar Wilde quotes web app

from django.urls import path                                                                                                          
from . import views                                                                                                                   
                                                                                                                                        
urlpatterns = [       
    path('', views.quote, name='quote'),                                                                                 
    path('quote/', views.quote, name='quote'),                                                                       
    path('show_all/', views.show_all, name='show_all'),                                                          
    path('about/', views.about, name='about'),                                                                                                                  
]                                                                                                                                     
     