# File: models.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/19/2026
# Description: Data models for the mini_insta application

from django.db import models
from django.urls import reverse

class Profile(models.Model):
    username = models.CharField(max_length=32, unique=True)
    display_name = models.CharField(max_length=32)
    profile_image_url = models.URLField(max_length=256) 
    bio_text = models.TextField(max_length=256)
    join_date = models.DateField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return f"Profile: username='{self.username}', display name='{self.display_name}',"
    
    def get_all_posts(self):
         '''Return all of the posts on this profile.'''
         posts = Post.objects.filter(profile=self)
         return posts

class Post(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(max_length=256,blank=True)

    def __str__(self):
        return f"Post: profile='{self.profile}', timestamp='{self.timestamp}'"
    
    def get_all_photos(self):
        '''Return all of the photos on this post.'''
        photos = Photo.objects.filter(post=self)
        return photos

    def get_absolute_url(self):
        '''Return the URL to display this post.'''
        return reverse('show_post', kwargs={'pk': self.pk})


class Photo(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f"Photo: post='{self.post}', image url = '{self.get_image_url()}'"
    
    def get_image_url(self):
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url