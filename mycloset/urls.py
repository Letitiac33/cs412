from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (HomeView, ClothingItemListView, AddClothingItemView,
                    ClothingItemDetailView, DeleteClothingItemView, StealItemView,
                    OutfitListView, OutfitDetailView, DeleteOutfitView,
                    OutfitBuilderView, SaveOutfitView, RateOutfitView,
                    ProfileDetailView, UpdateProfileView, FriendListView, AllUsersView,
                    StyleFeedView, PublicProfileView, SendFriendRequestView,
                    AcceptFriendRequestView, UnfriendView, CreateProfileView)

urlpatterns = [
    path('', HomeView.as_view(), name='mycloset_home'),
    path('closet/', ClothingItemListView.as_view(), name='mycloset_closet'),
    path('add/', AddClothingItemView.as_view(), name='mycloset_add'),
    path('item/<int:pk>/', ClothingItemDetailView.as_view(), name='mycloset_item_detail'),
    path('item/<int:pk>/delete/', DeleteClothingItemView.as_view(), name='mycloset_item_delete'),
    path('item/<int:pk>/steal/', StealItemView.as_view(), name='mycloset_item_steal'),
    path('outfits/', OutfitBuilderView.as_view(), name='mycloset_outfits'),
    path('outfit/<int:pk>/', OutfitDetailView.as_view(), name='mycloset_outfit_detail'),
    path('outfit/<int:pk>/delete/', DeleteOutfitView.as_view(), name='mycloset_outfit_delete'),
    path('outfit/<int:pk>/rate/', RateOutfitView.as_view(), name='mycloset_outfit_rate'),
    path('outfit/new/', OutfitBuilderView.as_view(), name='mycloset_outfit_builder'),
    path('outfit/<int:pk>/edit/', OutfitBuilderView.as_view(), name='mycloset_outfit_edit'),
    path('outfit/save/', SaveOutfitView.as_view(), name='mycloset_outfit_save'),
    path('signup/', CreateProfileView.as_view(), name='mycloset_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mycloset/login.html'), name='mycloset_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mycloset_logout_confirmation'), name='mycloset_logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mycloset/logged_out.html'), name='mycloset_logout_confirmation'),
    path('feed/', StyleFeedView.as_view(), name='mycloset_feed'),
    path('users/', AllUsersView.as_view(), name='mycloset_all_users'),
    path('user/<int:pk>/', PublicProfileView.as_view(), name='mycloset_public_profile'),
    path('user/<int:pk>/friend-request/', SendFriendRequestView.as_view(), name='mycloset_friend_request'),
    path('user/<int:pk>/accept-request/', AcceptFriendRequestView.as_view(), name='mycloset_accept_request'),
    path('user/<int:pk>/unfriend/', UnfriendView.as_view(), name='mycloset_unfriend'),
    path('profile/', ProfileDetailView.as_view(), name='mycloset_profile'),
    path('friends/', FriendListView.as_view(), name='mycloset_friends'),
    path('profile/edit/', UpdateProfileView.as_view(), name='mycloset_update_profile'),
]
