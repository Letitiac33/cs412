# File: models.py
# Description: Data models for the mycloset application

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    '''Represents a user profile.'''

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mycloset_profiles')
    username = models.CharField(max_length=32, unique=True)
    profile_image = models.ImageField(upload_to='mycloset/profiles/', blank=True)
    bio = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.username}"

class ClothingItem(models.Model):
    '''Represents a single clothing item uploaded by the user.'''

    class ClothingType(models.TextChoices):
        TOP = 'TOP', 'Top'
        BOTTOM = 'BOTTOM', 'Bottom'
        DRESS = 'DRESS', 'Dress'
        SHOES = 'SHOES', 'Shoes'
        ACCESSORY = 'ACCESSORY', 'Accessory'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=16, choices=ClothingType.choices)
    uploaded_image = models.ImageField(upload_to='mycloset/uploaded/')
    processed_image = models.ImageField(upload_to='mycloset/processed/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Friend(models.Model):
    '''Represents a friend request between two users.'''

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DECLINED = 'DECLINED', 'Declined'

    requesting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    responding_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requesting_user} -> {self.responding_user} ({self.status})"

class Outfit(models.Model):
    '''Represents an outfit composed of clothing items.
    Must have either a top + bottom, or a dress — not both.
    Must always have shoes and an accessory.
    '''

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    top = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='outfit_as_top')
    bottom = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='outfit_as_bottom')
    shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfit_as_shoes')
    accessory = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='outfit_as_accessory')

    def __str__(self):
        return f"{self.name} - ({self.user})"

class Rating(models.Model):
    '''Represents a rating given by a user to an outfit.'''

    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} rated {self.outfit} {self.rating}/5"
