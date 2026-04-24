import os
import json
from django.conf import settings
from django.views.generic import TemplateView, ListView, View, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from .models import ClothingItem, Outfit
from .forms import ClothingItemForm
from .utils import remove_background

DOLL_URL = settings.MEDIA_URL + 'mycloset/dolls/doll_pose_1.png'

SLOT_KEYS = [('TOP', 'top'), ('BOTTOM', 'bottom'), ('SHOES', 'shoes'), ('ACCESSORY', 'accessory')]


class MyClosetLoginRequiredMixin(LoginRequiredMixin):
    """Redirects unauthenticated users to the mycloset login page."""
    login_url = reverse_lazy('mycloset_login')


class HomeView(MyClosetLoginRequiredMixin, TemplateView):
    template_name = 'mycloset/home.html'


class ClothingItemListView(MyClosetLoginRequiredMixin, ListView):
    """Lists all clothing items belonging to the logged-in user's profile."""
    template_name = 'mycloset/closet.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        profile = self.request.user.mycloset_profiles.first()
        return ClothingItem.objects.filter(profile=profile)


class AddClothingItemView(MyClosetLoginRequiredMixin, CreateView):
    """Handles clothing item upload and background removal."""
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

        base = os.path.splitext(os.path.basename(item.uploaded_image.name))[0]
        item.processed_image.save(base + '_no_bg.png', ContentFile(processed_bytes), save=True)

        return super().form_valid(form)


class SaveOutfitView(MyClosetLoginRequiredMixin, View):
    """Creates or updates an outfit from the drag-and-drop builder payload."""

    def post(self, request):
        data = json.loads(request.body)
        profile = request.user.mycloset_profiles.first()

        # Index placed items by type so we can look up TOP, BOTTOM, etc. directly
        items = {i['type']: i for i in data.get('items', [])}

        if 'TOP' not in items or 'BOTTOM' not in items:
            return JsonResponse({'error': 'Top and bottom are required.'}, status=400)

        # Build a flat dict of model field names from the builder payload.
        # Each slot contributes _id (FK), _x, _y, _width, _height; absent slots are cleared to None.
        fields = {'name': data.get('name', 'My Outfit')}
        for slot, key in SLOT_KEYS:
            d = items.get(slot)
            if d:
                fields[key + '_id'] = d['pk']
                fields[key + '_x'] = d['x']
                fields[key + '_y'] = d['y']
                fields[key + '_width'] = d['width']
                fields[key + '_height'] = d['height']
            else:
                for suffix in ('_id', '_x', '_y', '_width', '_height'):
                    fields[key + suffix] = None

        # outfit_pk is present when editing an existing outfit; absent when creating a new one
        outfit_pk = data.get('outfit_pk')
        if outfit_pk:
            outfit = Outfit.objects.get(pk=outfit_pk, profile=profile)
            for k, v in fields.items():
                setattr(outfit, k, v)
            outfit.save()
        else:
            outfit = Outfit.objects.create(profile=profile, **fields)

        return JsonResponse({'id': outfit.pk})


class OutfitListView(MyClosetLoginRequiredMixin, ListView):
    """Lists all outfits belonging to the logged-in user's profile."""
    template_name = 'mycloset/outfits.html'
    context_object_name = 'outfits'

    def get_queryset(self):
        profile = self.request.user.mycloset_profiles.first()
        return Outfit.objects.filter(profile=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doll_url'] = DOLL_URL
        return context


class OutfitDetailView(MyClosetLoginRequiredMixin, DetailView):
    """Shows a single outfit with its items listed. Owners see edit/delete controls."""
    model = Outfit
    template_name = 'mycloset/outfit_detail.html'
    context_object_name = 'outfit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doll_url'] = DOLL_URL
        context['is_owner'] = self.object.profile == self.request.user.mycloset_profiles.first()
        return context


class OutfitBuilderView(MyClosetLoginRequiredMixin, ListView):
    """Drag-and-drop outfit builder. When pk is in the URL, pre-loads the existing outfit for editing."""
    template_name = 'mycloset/outfit_builder.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        # Sidebar only shows the current user's own clothing items
        profile = self.request.user.mycloset_profiles.first()
        return ClothingItem.objects.filter(profile=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doll_url'] = DOLL_URL

        # pk is only present in the URL when editing an existing outfit (/outfit/<pk>/edit/)
        outfit_pk = self.kwargs.get('pk')
        if outfit_pk:
            # Serialize the existing outfit to JSON so the builder JS can
            # pre-place each item at its saved position and size on page load
            outfit = Outfit.objects.get(pk=outfit_pk)
            items = []
            for slot, type_key in SLOT_KEYS:
                item = getattr(outfit, slot)
                if item:
                    items.append({
                        'pk': item.pk,
                        'type': type_key,
                        'src': item.processed_image.url,
                        'x': getattr(outfit, slot + '_x') or 0,
                        'y': getattr(outfit, slot + '_y') or 0,
                        'width': getattr(outfit, slot + '_width') or 80,
                        'height': getattr(outfit, slot + '_height') or 80,
                    })
            context['outfit_json'] = json.dumps({'pk': outfit.pk, 'name': outfit.name, 'items': items})
            context['cancel_url'] = reverse_lazy('mycloset_outfit_detail', kwargs={'pk': outfit_pk})
        else:
            # null tells the builder JS there is no outfit to pre-load
            context['outfit_json'] = 'null'
            context['cancel_url'] = reverse_lazy('mycloset_outfits')

        return context


class ClothingItemDetailView(MyClosetLoginRequiredMixin, DetailView):
    """Shows item detail. GET renders the page; POST updates the item name."""
    model = ClothingItem
    template_name = 'mycloset/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        context['outfit_count'] = Outfit.objects.filter(
            Q(top=item) | Q(bottom=item) | Q(shoes=item) | Q(accessory=item)
        ).count()
        return context

    def post(self, request, pk):
        item = get_object_or_404(ClothingItem, pk=pk)
        if item.profile != request.user.mycloset_profiles.first():
            return HttpResponseForbidden()
        name = request.POST.get('name', '').strip()
        if name:
            item.name = name
            item.save()
        return redirect('mycloset_item_detail', pk=pk)


class DeleteClothingItemView(MyClosetLoginRequiredMixin, View):
    """Deletes a clothing item (and any outfits containing it via cascade)."""

    def post(self, request, pk):
        item = get_object_or_404(ClothingItem, pk=pk)
        if item.profile == request.user.mycloset_profiles.first():
            item.delete()
        return redirect('mycloset_closet')


class DeleteOutfitView(MyClosetLoginRequiredMixin, View):
    """Deletes an outfit."""

    def post(self, request, pk):
        outfit = get_object_or_404(Outfit, pk=pk)
        if outfit.profile == request.user.mycloset_profiles.first():
            outfit.delete()
        return redirect('mycloset_outfits')
