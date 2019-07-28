from django.contrib import admin
from . import models

#be able to edit groups as and administrator. Dont need to register
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember


admin.site.register(models.Group)
