from django import template
from discussions.models import GroupMembership

register = template.Library()

@register.simple_tag
def is_member(user, group):
    """Checks if a user is a member of a specific group."""
    if not user or not user.is_authenticated:
        return False
    return GroupMembership.objects.filter(user=user, group=group).exists() 