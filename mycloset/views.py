import os
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from .models import ClothingItem
from .forms import ClothingItemForm
from .utils import remove_background


class MyClosetLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('mycloset_login')


class HomeView(MyClosetLoginRequiredMixin, TemplateView):
    template_name = 'mycloset/home.html'


class ClothingItemListView(MyClosetLoginRequiredMixin, ListView):
    template_name = 'mycloset/closet.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        profile = self.request.user.mycloset_profiles.first()
        return ClothingItem.objects.filter(profile=profile)


class AddClothingItemView(MyClosetLoginRequiredMixin, CreateView):
    model = ClothingItem
    form_class = ClothingItemForm
    template_name = 'mycloset/add_clothing.html'
    success_url = reverse_lazy('mycloset_closet')

    def form_valid(self, form):
        item = form.save(commit=False)
        item.profile = self.request.user.mycloset_profiles.first()
        item.save()

        with open(item.uploaded_image.path, 'rb') as f:
            processed_bytes = remove_background(f)

        filename = os.path.splitext(os.path.basename(item.uploaded_image.name))[0] + '_no_bg.png'
        item.processed_image.save(filename, ContentFile(processed_bytes), save=True)

        return super().form_valid(form)
