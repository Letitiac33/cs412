# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/12/2026
# Description: Views for the mini_insta application

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
from .models import Post

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'