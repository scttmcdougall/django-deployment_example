#POSTS VIEWS.py
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model

#call things off "user" in html
User = get_user_model()

#see a list of all posts for a user or group (select_related)
class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    #mixin that allows you to provide a tuple of a related model
    select_related = ('user','group')

#show user posts - list view for a users post
class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        #out of the query set (all posts) - return the posts of the user who is loggedin
        try:
            #users get_user_model
            self.post_user = User.objects.prefetch_related('posts').get(
            username__iexact=self.kwargs.get('username')
            )


        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    #returns the context dictionary
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

#show post detail
class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')
    #filter user name of the post is the user logged in
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin, SelectRelatedMixin,generic.CreateView):
    fields = ('message','group')
    model = models.Post
    #check of form is valid
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        #return message saying the post was deleted
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
