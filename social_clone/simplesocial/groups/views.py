

#GROUPS!!

from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                       PermissionRequiredMixin)
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views import generic
#class based views
from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    #fields the user is able to edit
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group


#login is required to do this. Once you join a group it redirects you somewhere
class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    #once joined a group redirect to groups single detail page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    #makes sure cant join a group if you're not already in it
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        #checks if already a member
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        #advises already member if exists already
        except IntegrityError:
            messages.warning(self.request,'Warning already a member')
        #else advise you've become a member
        else:
            messages.success(self.request,'You are now a member')

        return super().get(request,*args,**kwargs)


#login is required to do this. Once leave a group it redirects you somewhere
class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    #once leave a group redirect to groups single detail page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    #makes sure cant leave a group if you're not already in it
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        #checks if already a member
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()

        #advises already member if exists already
        except models.GroupMember.DoesNotExist:
                messages.warning(
                    self.request,
                    'sorry you arent in this group'
                )
        #else advise you've become a member
        else:
            membership.delete()
            messages.success(
                self.request,
                'you have left the group'
            )

        return super().get(request, *args, **kwargs)
