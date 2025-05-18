from django.db import models
from django.conf import settings

# Create your models here.

class DiscussionGroup(models.Model):
    """
    Represents a discussion group centered around a specific content item.

    Attributes:
        name (CharField): The name of the discussion group.
        description (TextField): A detailed description of the group.
        content_item (ForeignKey): The content item this group is about.
        creator (ForeignKey): The user who created the group.
        members (ManyToManyField): Users who are members of this group, managed via GroupMembership.
        created_at (DateTimeField): Timestamp of when the group was created.
        is_private (BooleanField): Indicates if the group is private or public.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content_item = models.ForeignKey(
        'content.ContentItem', 
        on_delete=models.CASCADE, 
        related_name='discussion_groups'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # If creator is deleted, group remains, creator becomes NULL
        null=True,
        related_name='created_discussion_groups'
    )
    # The old ManyToManyField for members is removed.
    # Members are now managed through the GroupMembership model.
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='GroupMembership', # Specify the intermediate model
        through_fields=('group', 'user'), # Explicitly define join fields if names are non-standard or for clarity
        related_name='discussion_groups_joined', # New related_name to avoid clashes
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['creator', 'name'], name='unique_group_name_per_creator')
        ]

    def __str__(self):
        return f"{self.name} (for: {self.content_item.title})"

class GroupMembership(models.Model):
    """
    Intermediate model to manage user membership in discussion groups and their roles.

    Attributes:
        user (ForeignKey): The user who is a member of the group.
        group (ForeignKey): The discussion group the user is a member of.
        date_joined (DateTimeField): Timestamp of when the user joined the group.
        role (CharField): The role of the user in the group (e.g., 'admin', 'member').
    """
    ROLE_ADMIN = 'admin'
    ROLE_MEMBER = 'member'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MEMBER, 'Member'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='discussion_group_roles')
    group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, related_name='membership_details')
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_MEMBER,
        help_text="The role of the user in this group."
    )

    class Meta:
        unique_together = ('user', 'group') # Ensure a user can only join a group once
        ordering = ['date_joined']
        verbose_name = "Group Membership"
        verbose_name_plural = "Group Memberships"

    def __str__(self):
        return f"{self.user.username} in {self.group.name} as {self.get_role_display()}"

class GroupPost(models.Model):
    """
    Represents a post or a reply within a discussion group (distinct from chat messages).
    This model seems to be for a forum-like feature within groups.

    Attributes:
        group (ForeignKey): The discussion group this post belongs to.
        author (ForeignKey): The user who created the post.
        content (TextField): The textual content of the post.
        created_at (DateTimeField): Timestamp of when the post was created.
        parent_post (ForeignKey): If this post is a reply, links to the parent post.
    """
    group = models.ForeignKey(DiscussionGroup, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='group_posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_post = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Post by {self.author.username} in {self.group.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
