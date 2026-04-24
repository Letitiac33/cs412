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
        SHOES = 'SHOES', 'Shoes'
        ACCESSORY = 'ACCESSORY', 'Accessory'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=16, choices=ClothingType.choices)
    uploaded_image = models.ImageField(upload_to='mycloset/uploaded/')
    processed_image = models.ImageField(upload_to='mycloset/processed/', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class FriendRequest(models.Model):
    '''Represents a friend request between two users.'''

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DECLINED = 'DECLINED', 'Declined'

    requesting_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_requests')
    responding_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requesting_profile} -> {self.responding_profile} ({self.status})"

    def accept(self):
        '''Accepts the friend request and creates a Friendship.'''
        if self.status == self.Status.PENDING:
            self.status = self.Status.ACCEPTED
            self.save()
            Friendship.objects.create(profile1=self.requesting_profile, profile2=self.responding_profile)
    
    def decline(self):
        '''Declines the friend request.'''
        if self.status == self.Status.PENDING:
            self.status = self.Status.DECLINED
            self.save()

class Friendship(models.Model):
    '''Represents a friendship between two users.'''

    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendship_profile2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile1} & {self.profile2}"
    
class Outfit(models.Model):
    '''Represents an outfit composed of clothing items.'''

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    top = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='outfit_as_top')
    top_x = models.IntegerField(null=True, blank=True)
    top_y = models.IntegerField(null=True, blank=True)
    top_width = models.PositiveIntegerField(null=True, blank=True)
    top_height = models.PositiveIntegerField(null=True, blank=True)

    bottom = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name='outfit_as_bottom')
    bottom_x = models.IntegerField(null=True, blank=True)
    bottom_y = models.IntegerField(null=True, blank=True)
    bottom_width = models.PositiveIntegerField(null=True, blank=True)
    bottom_height = models.PositiveIntegerField(null=True, blank=True)

    shoes = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, related_name='outfit_as_shoes')
    shoes_x = models.IntegerField(null=True, blank=True)
    shoes_y = models.IntegerField(null=True, blank=True)
    shoes_width = models.PositiveIntegerField(null=True, blank=True)
    shoes_height = models.PositiveIntegerField(null=True, blank=True)

    accessory = models.ForeignKey(ClothingItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='outfit_as_accessory')
    accessory_x = models.IntegerField(null=True, blank=True)
    accessory_y = models.IntegerField(null=True, blank=True)
    accessory_width = models.PositiveIntegerField(null=True, blank=True)
    accessory_height = models.PositiveIntegerField(null=True, blank=True)

    DOLL_CENTER_X = 197

    # @property lets templates use {{ outfit.shoes_left_x }} like a field instead of a method call
    @property
    def shoes_left_x(self):
        if self.shoes_x is not None and self.shoes_width:
            return 2 * self.DOLL_CENTER_X - self.shoes_x - self.shoes_width
        return None

    def __str__(self):
        return f"{self.name} - ({self.profile})"

class Rating(models.Model):
    '''Represents a rating given by a user to an outfit.'''

    rater = models.ForeignKey(Profile, on_delete=models.CASCADE)
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rater} rated {self.outfit} {self.rating}/5"
