# File: views.py
# Author: Letitia Caspersen (letitiac@bu.edu), 2/27/2026
# Description: Views for the mini_insta application

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

class ProfileListView(ListView):
    '''Create a subclass of ListView to display all mini insta profiles.'''
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta profile.'''
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Create a subclass of DetailView to display a single mini insta post.'''
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''Create a subclass of CreateView to handle creating a new Post.'''
    template_name = 'mini_insta/create_post_form.html'
    form_class = CreatePostForm

    def get_context_data(self, **kwargs):
        '''Add the Profile object to the context so the template can build the form action URL.'''
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Attach the Profile foreign key to the Post, then create a Photo for the post.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
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
    
class UpdateProfileView(UpdateView):
    template_name = 'mini_insta/update_profile_form.html'
    form_class = UpdateProfileForm
    model = Profile
    context_object_name = 'profile'

class DeletePostView(DeleteView):
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

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'mini_insta/update_post_form.html'
    form_class = UpdatePostForm
    context_object_name = 'post'

    def get_success_url(self):
        '''Redirect to the post page after a successful update.'''
        return reverse('show_post', kwargs={'pk': self.object.pk})

class PostFeedListView(ListView):
    '''Display the post feed for a single Profile.'''
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''Return the post feed for the profile.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        '''Add the profile to the context.'''
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
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

class SearchView(ListView):
    '''Search profiles and posts based on a text query.'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''If no query is present, show the search form. Otherwise, continue to ListView.'''
        if 'query' not in request.GET:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        '''Return Posts whose caption contains the query.'''
        query = self.request.GET['query']
        return Post.objects.filter(caption__icontains=query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET['query']
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        context['query'] = query
        context['profiles'] = (
            Profile.objects.filter(username__icontains=query) |
            Profile.objects.filter(display_name__icontains=query) |
            Profile.objects.filter(bio_text__icontains=query)
        )
        return context
