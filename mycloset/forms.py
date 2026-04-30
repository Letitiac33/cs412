from django import forms
from .models import ClothingItem, Profile


class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['name', 'type', 'uploaded_image']


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'bio', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'profile_image', 'bio']
        widgets = {
            'profile_image': forms.FileInput(),
        }
