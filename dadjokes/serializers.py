# File: serializers.py
# Author: Letitia Caspersen (letitiac@bu.edu), 4/3/2026
# Description: Serializers for the dadjokes REST API

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    '''A serializer for the Joke model.'''

    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    '''A serializer for the Picture model.'''

    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'timestamp']
