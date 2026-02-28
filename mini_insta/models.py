# File: models.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/27/2026
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
        return f"{self.username}"
    
    def get_all_posts(self):
         '''Return all of the posts on this profile.'''
         posts = Post.objects.filter(profile=self)
         return posts
    
    def get_followers(self):
        '''Return a list of Profiles who follow this profile.'''
        follows = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in follows]

    def get_num_followers(self):
        '''Return the number of followers for this profile.'''
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a list of Profiles that this profile is following.'''
        follows = Follow.objects.filter(follower_profile=self)
        return [follow.profile for follow in follows]

    def get_num_following(self):
        '''Return the number of profiles this profile is following.'''
        return Follow.objects.filter(follower_profile=self).count()

    def get_absolute_url(self):
        '''Return the URL to display this profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})

class Post(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(max_length=256,blank=True)

    def __str__(self):
        return f"Post: '{self.profile}: {self.caption}'"
    
    def get_all_photos(self):
        '''Return all of the photos on this post.'''
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_all_comments(self):
        '''Return all of the comments on this post.'''
        comments = Comment.objects.filter(post=self)
        return comments

    def get_absolute_url(self):
        '''Return the URL to display this post.'''
        return reverse('show_post', kwargs={'pk': self.pk})


class Photo(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f"Photo: '{self.post} Picture: {self.pk}'"
    
    def get_image_url(self):
        '''Return the appropriate image url based on upload method used.'''
        if self.image_url:
            return self.image_url
        else:
            return self.image_file.url

class Follow(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile} follows {self.profile}"
    
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(max_length=512,blank=True)

    def __str__(self):
        return f"Comment: '{self.profile.username}: {self.text}'"