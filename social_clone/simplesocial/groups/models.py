#GROUPS - models!
from django.conf import settings
#from django.core.urlresolvers import reverse
from django.urls import reverse

from django.db import models
#allows remove characters that are alphnumeric (eg. spaces in urls, allow to work with browser)
from django.utils.text import slugify

#allows link embedding - needs MS visual C++ 14.0
#import misaka

#returns user model currently active - allows call things off the current user session
from django.contrib.auth import get_user_model

User = get_user_model()

#users custom template tags
from django import template
register=template.Library()


class Group(models.Model):
    #name of the group
    name = models.CharField(max_length=255,unique=True)
    #slug representation of the group
    slug = models.SlugField(allow_unicode=True,unique=True)
    #description of the group
    description = models.TextField(blank=True,default='')
    #use to get markdown text
    description_html = models.TextField(editable=False,default='',blank=True)
    #list of members that below to the group
    members = models.ManyToManyField(User,through="GroupMember")

    #returns the group name
    def __str__(self):
        return self.name

    #used to save a new group
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        #self.description_html = misaka.html(self.description)
        self.description_html = self.description
        super().save(*args,**kwargs)

    #once a group is created - where is the user sent?
    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    #call to order the list of groups by alpha by name
    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    #group user belongs too
    group = models.ForeignKey(Group,related_name="memberships",on_delete=models.CASCADE)
    #user whos part of the group
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group','user')
    #pass
