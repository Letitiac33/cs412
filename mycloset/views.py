import os
import json
from django.conf import settings
from django.views.generic import TemplateView, ListView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q, Avg
from .models import ClothingItem, Outfit, Profile, Friendship, FriendRequest, Rating
from .forms import ClothingItemForm, UpdateProfileForm, CreateProfileForm
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
        return Outfit.objects.filter(profile=profile).annotate(avg_rating=Avg('rating__rating'))

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
        my_profile = self.request.user.mycloset_profiles.first()
        context['doll_url'] = DOLL_URL
        context['is_owner'] = self.object.profile == my_profile
        ratings = Rating.objects.filter(outfit=self.object)
        context['rating_count'] = ratings.count()
        context['avg_rating'] = round(sum(r.rating for r in ratings) / ratings.count(), 1) if ratings.count() else None
        context['my_rating'] = ratings.filter(rater=my_profile).first()
        return context


class RateOutfitView(MyClosetLoginRequiredMixin, View):
    """Creates or updates the logged-in user's rating for an outfit."""

    def post(self, request, pk):
        outfit = get_object_or_404(Outfit, pk=pk)
        my_profile = request.user.mycloset_profiles.first()
        value = int(request.POST.get('rating', 0))
        if 1 <= value <= 5 and outfit.profile != my_profile:
            Rating.objects.update_or_create(
                rater=my_profile, outfit=outfit,
                defaults={'rating': value}
            )
        return redirect('mycloset_outfit_detail', pk=pk)


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
            context['cancel_url'] = reverse_lazy('mycloset_profile')

        return context


class ClothingItemDetailView(MyClosetLoginRequiredMixin, DetailView):
    """Shows item detail. GET renders the page; POST updates the item name."""
    model = ClothingItem
    template_name = 'mycloset/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        my_profile = self.request.user.mycloset_profiles.first()
        context['is_owner'] = item.profile == my_profile
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


class StealItemView(MyClosetLoginRequiredMixin, View):
    """Copies another user's clothing item into the logged-in user's closet."""

    def post(self, request, pk):
        original = get_object_or_404(ClothingItem, pk=pk)
        my_profile = request.user.mycloset_profiles.first()

        if original.profile == my_profile:
            return redirect('mycloset_item_detail', pk=pk)

        new_item = ClothingItem(
            profile=my_profile,
            name=original.name,
            type=original.type,
        )

        # Copy the uploaded image
        original.uploaded_image.open('rb')
        new_item.uploaded_image.save(
            os.path.basename(original.uploaded_image.name),
            ContentFile(original.uploaded_image.read()),
            save=False,
        )
        original.uploaded_image.close()

        # Copy the processed image if it exists
        if original.processed_image:
            original.processed_image.open('rb')
            new_item.processed_image.save(
                os.path.basename(original.processed_image.name),
                ContentFile(original.processed_image.read()),
                save=False,
            )
            original.processed_image.close()

        new_item.save()
        return redirect('mycloset_closet')


class DeleteOutfitView(MyClosetLoginRequiredMixin, View):
    """Deletes an outfit."""

    def post(self, request, pk):
        outfit = get_object_or_404(Outfit, pk=pk)
        if outfit.profile == request.user.mycloset_profiles.first():
            outfit.delete()
        return redirect('mycloset_profile')


class ProfileDetailView(MyClosetLoginRequiredMixin, DetailView):
    """Shows the logged-in user's profile."""
    model = Profile
    template_name = 'mycloset/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.mycloset_profiles.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['clothing_count'] = ClothingItem.objects.filter(profile=profile).count()
        context['outfits'] = Outfit.objects.filter(profile=profile).annotate(avg_rating=Avg('rating__rating')).order_by('-pk')
        context['outfit_count'] = context['outfits'].count()
        context['friend_count'] = Friendship.objects.filter(Q(profile1=profile) | Q(profile2=profile)).count()
        context['doll_url'] = DOLL_URL
        return context


class UpdateProfileView(MyClosetLoginRequiredMixin, UpdateView):
    """Lets the logged-in user edit their profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mycloset/update_profile.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('mycloset_profile')

    def get_object(self):
        return self.request.user.mycloset_profiles.first()


class CreateProfileView(CreateView):
    """Creates a new User and linked Profile, then logs the user in."""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mycloset/create_profile.html'
    success_url = reverse_lazy('mycloset_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in kwargs:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)


class AllUsersView(MyClosetLoginRequiredMixin, View):
    """Lists every profile on the platform."""

    def get(self, request):
        my_profile = request.user.mycloset_profiles.first()
        profiles = Profile.objects.exclude(pk=my_profile.pk).order_by('username')
        return render(request, 'mycloset/all_users.html', {'profiles': profiles})


class FriendListView(MyClosetLoginRequiredMixin, View):
    """Shows all friends of the logged-in user."""

    def get(self, request):
        profile = request.user.mycloset_profiles.first()
        friendships = Friendship.objects.filter(Q(profile1=profile) | Q(profile2=profile))
        friends = [
            f.profile2 if f.profile1 == profile else f.profile1
            for f in friendships
        ]
        return render(request, 'mycloset/friends.html', {'friends': friends})


class StyleFeedView(MyClosetLoginRequiredMixin, View):
    """Shows outfits from friends, with a profile search bar."""

    def get(self, request):
        profile = request.user.mycloset_profiles.first()

        friendships = Friendship.objects.filter(Q(profile1=profile) | Q(profile2=profile))
        friend_profiles = [
            f.profile2 if f.profile1 == profile else f.profile1
            for f in friendships
        ]
        outfits = Outfit.objects.filter(profile__in=friend_profiles).annotate(avg_rating=Avg('rating__rating')).order_by('-id')

        incoming = FriendRequest.objects.filter(
            responding_profile=profile,
            status=FriendRequest.Status.PENDING
        ).select_related('requesting_profile')

        context = {'outfits': outfits, 'doll_url': DOLL_URL, 'incoming_requests': incoming}

        q = request.GET.get('q', '').strip()
        if q:
            context['search_results'] = Profile.objects.filter(
                username__icontains=q
            ).exclude(pk=profile.pk)
            context['query'] = q

        return render(request, 'mycloset/feed.html', context)


class PublicProfileView(MyClosetLoginRequiredMixin, DetailView):
    """Shows another user's profile with friend status."""
    model = Profile
    template_name = 'mycloset/public_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_profile = self.request.user.mycloset_profiles.first()
        their_profile = self.object

        context['outfits'] = Outfit.objects.filter(profile=their_profile).annotate(avg_rating=Avg('rating__rating'))
        context['outfit_count'] = context['outfits'].count()
        context['clothing_count'] = ClothingItem.objects.filter(profile=their_profile).count()
        context['doll_url'] = DOLL_URL

        context['is_friend'] = Friendship.objects.filter(
            Q(profile1=my_profile, profile2=their_profile) |
            Q(profile1=their_profile, profile2=my_profile)
        ).exists()

        context['request_sent'] = FriendRequest.objects.filter(
            requesting_profile=my_profile,
            responding_profile=their_profile,
            status=FriendRequest.Status.PENDING
        ).exists()

        context['incoming_request'] = FriendRequest.objects.filter(
            requesting_profile=their_profile,
            responding_profile=my_profile,
            status=FriendRequest.Status.PENDING
        ).first()

        return context


class SendFriendRequestView(MyClosetLoginRequiredMixin, View):
    """Sends a friend request to another profile."""

    def post(self, request, pk):
        my_profile = request.user.mycloset_profiles.first()
        their_profile = get_object_or_404(Profile, pk=pk)
        already_friends = Friendship.objects.filter(
            Q(profile1=my_profile, profile2=their_profile) |
            Q(profile1=their_profile, profile2=my_profile)
        ).exists()
        already_requested = FriendRequest.objects.filter(
            requesting_profile=my_profile,
            responding_profile=their_profile,
            status=FriendRequest.Status.PENDING
        ).exists()
        if not already_friends and not already_requested:
            FriendRequest.objects.create(
                requesting_profile=my_profile,
                responding_profile=their_profile
            )
        return redirect('mycloset_public_profile', pk=pk)


class AcceptFriendRequestView(MyClosetLoginRequiredMixin, View):
    """Accepts an incoming friend request."""

    def post(self, request, pk):
        my_profile = request.user.mycloset_profiles.first()
        friend_request = get_object_or_404(
            FriendRequest,
            requesting_profile__pk=pk,
            responding_profile=my_profile,
            status=FriendRequest.Status.PENDING
        )
        friend_request.accept()
        return redirect('mycloset_public_profile', pk=pk)


class UnfriendView(MyClosetLoginRequiredMixin, View):
    """Removes a friendship between the logged-in user and another profile."""

    def post(self, request, pk):
        my_profile = request.user.mycloset_profiles.first()
        their_profile = get_object_or_404(Profile, pk=pk)
        Friendship.objects.filter(
            Q(profile1=my_profile, profile2=their_profile) |
            Q(profile1=their_profile, profile2=my_profile)
        ).delete()
        return redirect('mycloset_public_profile', pk=pk)
