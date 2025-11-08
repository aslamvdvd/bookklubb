from django.contrib import admin
from .models import DiscussionGroup, GroupPost, GroupMembership

# Register your models here.
admin.site.register(DiscussionGroup)
admin.site.register(GroupPost)

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    """
    Admin configuration for the GroupMembership model.
    
    Displays user, group, role, and date_joined.
    Provides filtering by group, user, and role.
    Allows searching by user username and group name.
    Makes role editable in the list view for quick changes.
    """
    list_display = ('user', 'group', 'role', 'date_joined')
    list_filter = ('group', 'user', 'role', 'date_joined')
    search_fields = ('user__username', 'group__name')
    list_editable = ('role',)
    readonly_fields = ('date_joined',)
