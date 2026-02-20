# File: forms.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/19/2026
# Description: Forms for the mini_insta application

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database.'''

    image_url = forms.URLField(label='Image URL', required=False)

    class Meta:
        '''associate this form with a model from our database.'''
        model = Post
        fields = ['caption']
