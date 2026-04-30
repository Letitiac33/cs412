# File: forms.py
# Description: ModelForms for clothing items and user profiles

from django import forms
from .models import ClothingItem, Profile


class ClothingItemForm(forms.ModelForm):
    """Form for uploading a new clothing item."""
    class Meta:
        model = ClothingItem
        fields = ['name', 'type', 'uploaded_image']


class CreateProfileForm(forms.ModelForm):
    """Form for creating a new profile during sign-up."""
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(),
        }


class UpdateProfileForm(forms.ModelForm):
    """Form for editing an existing profile."""
    class Meta:
        model = Profile
        fields = ['username', 'profile_image', 'bio']
        widgets = {
            'profile_image': forms.FileInput(),
        }
