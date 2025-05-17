from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from discussions.models import DiscussionGroup

User = get_user_model()

@login_required
def dashboard_index(request, username):
    """Displays the user's dashboard, including their created and joined groups."""
    # Ensure the dashboard being viewed is for the logged-in user, 
    # or implement permission checks if users can view others' dashboards (not typical for this context).
    # For simplicity, we'll assume users only see their own dashboard details if request.user.username matches username path param.
    dashboard_user = get_object_or_404(User, username=username)

    # Ensure a user can only see sensitive parts of their own dashboard
    # If request.user != dashboard_user, you might show a limited public view or deny access.
    # For now, we proceed assuming it's the user viewing their own dashboard.

    created_groups = DiscussionGroup.objects.filter(creator=request.user).order_by('-created_at')
    
    # Use the correct related_name: discussion_groups_joined
    all_joined_groups = request.user.discussion_groups_joined.all().order_by('-created_at')
    
    # To get GroupMembership objects (with roles), you would use: request.user.discussion_group_roles.all()
    # Then iterate through those to get the actual group: membership.group

    # Refined logic for 'joined_groups_not_created_by_user'
    # This fetches DiscussionGroup instances directly
    joined_groups_not_created_by_user = request.user.discussion_groups_joined.exclude(creator=request.user).order_by('-created_at')

    context = {
        'dashboard_user': dashboard_user, # The user whose dashboard is being viewed
        'created_groups': created_groups,
        'joined_groups_not_created_by_user': joined_groups_not_created_by_user,
        'all_joined_groups': all_joined_groups, # Keep this for clarity on what it contains
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def dashboard_settings_view(request, username):
    """Placeholder view for user dashboard settings."""
    # Ensure the settings being viewed/edited are for the logged-in user
    dashboard_user = get_object_or_404(User, username=username)
    if request.user != dashboard_user:
        # Redirect or show an error if trying to access another user's settings
        # For now, let's redirect to their own dashboard or show a simple message.
        # A more robust solution would be a proper error page or message.
        return redirect('dashboard:index', username=request.user.username) 
        # Or: messages.error(request, "You can only view your own settings.")
        # return render(request, 'error_page.html', {'message': "Access Denied"})

    context = {
        'dashboard_user': dashboard_user,
    }
    # We'll need to create this template next
    return render(request, 'dashboard/settings.html', context)

@login_required
def user_groups_view(request, username):
    """Displays a page with the user's created and joined discussion groups."""
    display_user = get_object_or_404(User, username=username)

    # Optional: Add permission check if users can see other users' group lists.
    # For now, assuming a user is viewing their own or it's a public-enough list.
    # If strictly private, add: if request.user != display_user: return redirect('some_error_page_or_home')

    created_groups = DiscussionGroup.objects.filter(creator=display_user).order_by('-created_at')
    
    # Use the correct related_name: discussion_groups_joined
    joined_groups_not_created_by_user = display_user.discussion_groups_joined.exclude(creator=display_user).order_by('-created_at')

    context = {
        'display_user': display_user, # The user whose groups are being viewed
        'created_groups': created_groups,
        'joined_groups_not_created_by_user': joined_groups_not_created_by_user,
        'page_title': f"{display_user.first_name or display_user.username}'s Groups"
    }
    return render(request, 'dashboard/my_groups.html', context)
