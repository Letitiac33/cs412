# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 4/2/2026
# Description: View functions for the dadjokes application

from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture
import random

# REST API imports
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import JokeSerializer, PictureSerializer

def random_joke_and_picture(request):
    """Return an HTML page displaying one random Joke and one random Picture."""
    joke = random.choice(Joke.objects.all()) if Joke.objects.exists() else None
    picture = random.choice(Picture.objects.all()) if Picture.objects.exists() else None
    return render(request, 'dadjokes/random.html', {'joke': joke, 'picture': picture})

def all_jokes(request):
    """Return an HTML page displaying all Jokes."""
    jokes = Joke.objects.all()
    return render(request, 'dadjokes/jokes.html', {'jokes': jokes})

def one_joke(request, pk):
    """Return an HTML page displaying a single Joke by primary key."""
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke.html', {'joke': joke})

def all_pictures(request):
    """Return an HTML page displaying all Pictures."""
    pictures = Picture.objects.all()
    return render(request, 'dadjokes/pictures.html', {'pictures': pictures})

def one_picture(request, pk):
    """Return an HTML page displaying a single Picture by primary key."""
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture.html', {'picture': picture})


# REST API views

class RandomJokeAPIView(APIView):
    '''Returns a JSON representation of one Joke selected at random.'''

    def get(self, request):
        jokes = Joke.objects.all()
        joke = random.choice(jokes) if jokes.exists() else None
        if joke is None:
            return Response({'error': 'No jokes available.'}, status=404)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)


class JokeListAPIView(generics.ListCreateAPIView):
    '''Returns a JSON list of all Jokes; also accepts POST to create a new Joke.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    '''Returns a JSON representation of one Joke by primary key.'''
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    '''Returns a JSON list of all Pictures.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    '''Returns a JSON representation of one Picture by primary key.'''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(APIView):
    '''Returns a JSON representation of one Picture selected at random.'''

    def get(self, request):
        pictures = Picture.objects.all()
        picture = random.choice(pictures) if pictures.exists() else None
        if picture is None:
            return Response({'error': 'No pictures available.'}, status=404)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
