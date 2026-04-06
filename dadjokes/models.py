# File: models.py
# Author: Letitia Caspersen (letitiac@bu.edu), 4/2/2026
# Description: Data models for the dadjokes application

from django.db import models

class Joke(models.Model):
    text = models.TextField(max_length=256)
    contributor = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Joke.'''
        return f"Joke by {self.contributor} at {self.timestamp}"

class Picture(models.Model):
    image_url = models.URLField(max_length=256)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Picture.'''
        return f"Picture at {self.timestamp}"
