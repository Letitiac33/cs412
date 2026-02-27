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
