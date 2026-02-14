# File: models.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/12/2026
# Description: Data models for the mini_insta application

from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=32, unique=True)
    display_name = models.CharField(max_length=32)
    profile_image_url = models.URLField(max_length=256) 
    bio_text = models.TextField(max_length=256)
    join_date = models.DateField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return f"Profile: username='{self.username}', display name='{self.display_name}',"