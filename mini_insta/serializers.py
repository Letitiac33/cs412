# File: serializers.py
# Author: Letitia Caspersen (letitiac@bu.edu), 4/7/2026
# Description: Serializers for the mini_insta REST API

from rest_framework import serializers
from .models import Profile, Post, Photo

class ProfileSerializer(serializers.ModelSerializer):
    '''A serializer for the Profile model.'''

    class Meta:
        model = Profile
        fields = ['id', 'username', 'display_name', 'profile_image_url', 'bio_text', 'join_date']


class PhotoSerializer(serializers.ModelSerializer):
    '''A serializer for the Photo model.'''

    class Meta:
        model = Photo
        fields = ['id', 'image_url', 'image_file', 'timestamp']


class PostSerializer(serializers.ModelSerializer):
    '''A serializer for the Post model, including nested photos.'''
    photos = PhotoSerializer(source='photo_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'profile', 'caption', 'timestamp', 'photos']
