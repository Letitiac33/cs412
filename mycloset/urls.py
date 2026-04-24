from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import HomeView, ClothingItemListView, AddClothingItemView

urlpatterns = [
    path('', HomeView.as_view(), name='mycloset_home'),
    path('closet/', ClothingItemListView.as_view(), name='mycloset_closet'),
    path('add/', AddClothingItemView.as_view(), name='mycloset_add'),
    path('login/', auth_views.LoginView.as_view(template_name='mycloset/login.html'), name='mycloset_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mycloset_logout_confirmation'), name='mycloset_logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='mycloset/logged_out.html'), name='mycloset_logout_confirmation'),
]
