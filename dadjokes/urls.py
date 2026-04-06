# File: urls.py
# Author: Letitia Caspersen (letitiac@bu.edu), 4/2/2026
# Description: URL patterns for the dadjokes application

from django.urls import path
from . import views

urlpatterns = [
    # HTML views
    path('', views.random_joke_and_picture, name='dadjokes_home'),
    path('random', views.random_joke_and_picture, name='dadjokes_random'),
    path('jokes', views.all_jokes, name='dadjokes_jokes'),
    path('joke/<int:pk>', views.one_joke, name='dadjokes_joke'),
    path('pictures', views.all_pictures, name='dadjokes_pictures'),
    path('picture/<int:pk>', views.one_picture, name='dadjokes_picture'),

    # REST API views
    path('api/', views.RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', views.RandomJokeAPIView.as_view(), name='api_random_joke_2'),
    path('api/jokes', views.JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', views.JokeDetailAPIView.as_view(), name='api_joke'),
    path('api/pictures', views.PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', views.PictureDetailAPIView.as_view(), name='api_picture'),
    path('api/random_picture', views.RandomPictureAPIView.as_view(), name='api_random_picture'),
]
