from django.db import models
from django.conf import settings

# Create your models here.

class DiscussionGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_item = models.ForeignKey(
        'content.ContentItem', 
        on_delete=models.CASCADE, 
        related_name='discussion_groups'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_discussion_groups'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='discussion_group_memberships',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (for: {self.content_item.title})"

class GroupPost(models.Model):
    group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author.username} in {self.group.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
