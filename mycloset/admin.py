from django.contrib import admin
from .models import Profile, ClothingItem, FriendRequest, Friendship, Outfit, Rating

admin.site.register(Profile)
admin.site.register(ClothingItem)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(Outfit)
admin.site.register(Rating)
