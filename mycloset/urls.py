from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (HomeView, ClothingItemListView, AddClothingItemView,
                    ClothingItemDetailView, DeleteClothingItemView,
                    OutfitListView, OutfitDetailView, DeleteOutfitView,
                    OutfitBuilderView, SaveOutfitView)

urlpatterns = [
    path('', HomeView.as_view(), name='mycloset_home'),
    path('closet/', ClothingItemListView.as_view(), name='mycloset_closet'),
    path('add/', AddClothingItemView.as_view(), name='mycloset_add'),
    path('item/<int:pk>/', ClothingItemDetailView.as_view(), name='mycloset_item_detail'),
    path('item/<int:pk>/delete/', DeleteClothingItemView.as_view(), name='mycloset_item_delete'),
    path('outfits/', OutfitListView.as_view(), name='mycloset_outfits'),
    path('outfit/<int:pk>/', OutfitDetailView.as_view(), name='mycloset_outfit_detail'),
    path('outfit/<int:pk>/delete/', DeleteOutfitView.as_view(), name='mycloset_outfit_delete'),
    path('outfit/new/', OutfitBuilderView.as_view(), name='mycloset_outfit_builder'),
    path('outfit/<int:pk>/edit/', OutfitBuilderView.as_view(), name='mycloset_outfit_edit'),
    path('outfit/save/', SaveOutfitView.as_view(), name='mycloset_outfit_save'),
    path('login/', auth_views.LoginView.as_view(template_name='mycloset/login.html'), name='mycloset_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mycloset_logout_confirmation'), name='mycloset_logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mycloset/logged_out.html'), name='mycloset_logout_confirmation'),
]
