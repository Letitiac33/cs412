# File: forms.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/27/2026
# Description: Forms for the mini_insta application

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database.'''

    image_file = forms.ImageField(label='Image File', required=False)

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a users profile in the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''A form to update a post's caption in the database.'''

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']