# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/27/2026
# Description: Views for the mini_insta application

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import redirect
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class MiniInstaLoginRequiredMixin(LoginRequiredMixin):
    def get_logged_in_user_profile(self):
        '''Return the Profile associated with the currently logged-in user.'''
        return Profile.objects.filter(user=self.request.user).first()

    def get_login_url(self):
        '''Return the URL to the app's login page.'''
        return reverse('login')

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.filter(user=self.request.user).first()
        return context

class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            context['is_following'] = Follow.objects.filter(
                profile=self.object, follower_profile=logged_in_profile
            ).exists()
        return context

class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            logged_in_profile = Profile.objects.filter(user=self.request.user).first()
            context['is_liked'] = Like.objects.filter(
                post=self.object, profile=logged_in_profile
            ).exists()
        return context

class CreatePostView(MiniInstaLoginRequiredMixin, CreateView):
    '''Create a subclass of CreateView to handle creating a new Post.'''
    template_name = 'mini_insta/create_post_form.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context so the template can build the form action URL.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_user_profile()
        return context

    def form_valid(self, form):
        '''Attach the Profile foreign key to the Post, then create a Photo for the post.'''
        profile = self.get_logged_in_user_profile()
        form.instance.profile = profile
        response = super().form_valid(form)

        ### Deprecated Code ###
        # image_url = self.request.POST.get('image_url')
        # if image_url:
        #    Photo.objects.create(post=self.object, image_url=image_url)

        image_files = self.request.FILES.getlist('image_file')
        for image_file in image_files:
            Photo.objects.create(post=self.object, image_file=image_file)

        return response
    
class UpdateProfileView(MiniInstaLoginRequiredMixin, UpdateView):
    template_name = 'mini_insta/update_profile_form.html'
    form_class = UpdateProfileForm
    model = Profile
    context_object_name = 'profile'

    def get_object(self):
        '''Return the Profile of the logged-in user.'''
        return self.get_logged_in_user_profile()

class DeletePostView(MiniInstaLoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Build the context with post and profile'''
        context = super().get_context_data(**kwargs)
        post = self.object
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        '''Redirect to the profile page after a successful delete.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdatePostView(MiniInstaLoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'mini_insta/update_post_form.html'
    form_class = UpdatePostForm
    context_object_name = 'post'

    def get_success_url(self):
        '''Redirect to the post page after a successful update.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class PostFeedListView(MiniInstaLoginRequiredMixin, ListView):
    '''Display the post feed for a single Profile.'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''Return the post feed for the profile.'''
        return self.get_logged_in_user_profile().get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the profile to the context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_user_profile()
        return context

class ShowFollowersDetailView(DetailView):
    '''Display the followers of a Profile.'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''Display the profiles that a Profile is following.'''
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class CreateProfileView(CreateView):
    '''Create a new Profile and associated User account.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        '''Create the User, log them in, attach to the Profile, then save.'''
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

class ShowMyProfileView(MiniInstaLoginRequiredMixin, DetailView):
    '''Show the profile page for the currently logged-in user.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        '''Return the Profile of the logged-in user.'''
        return self.get_logged_in_user_profile()

class SearchView(MiniInstaLoginRequiredMixin, ListView):
    '''Search profiles and posts based on a text query.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''If no query is present, show the search form. Otherwise, continue to ListView.'''
        if 'query' not in request.GET:
            profile = Profile.objects.filter(user=request.user).first()
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts whose caption contains the query.'''
        query = self.request.GET['query']
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET['query']
        context['profile'] = self.get_logged_in_user_profile()
        context['query'] = query
        context['profiles'] = (
            Profile.objects.filter(username__icontains=query) |
            Profile.objects.filter(display_name__icontains=query) |
            Profile.objects.filter(bio_text__icontains=query)
        )
        return context

class FollowProfileView(MiniInstaLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        follower = self.get_logged_in_user_profile()
        Follow.objects.get_or_create(profile=profile, follower_profile=follower)
        return redirect('show_profile', pk=profile.pk)

class DeleteFollowView(MiniInstaLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        follower = self.get_logged_in_user_profile()
        Follow.objects.filter(profile=profile, follower_profile=follower).delete()
        return redirect('show_profile', pk=profile.pk)

class LikePostView(MiniInstaLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        liker = self.get_logged_in_user_profile()
        Like.objects.get_or_create(post=post, profile=liker)
        return redirect('show_post', pk=post.pk)

class DeleteLikeView(MiniInstaLoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        liker = self.get_logged_in_user_profile()
        Like.objects.filter(post=post, profile=liker).delete()
        return redirect('show_post', pk=post.pk)
