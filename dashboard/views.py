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
    joined_groups = request.user.discussion_group_memberships.all().order_by('-created_at')

    # To avoid showing groups in both lists if the creator is also a member (which they are by default):
    # We can get joined_groups that were not created by the user.
    # However, a user might want to see a group they created in their "joined" list too.
    # For now, we will keep them separate. If a group is created by user, it shows in 'created_groups'.
    # 'joined_groups' will show all groups they are a member of (including those they created).
    # A more refined approach might be: "My Groups (Created by Me)" and "Other Groups I'm In".
    # Or, simply, "All My Groups", and then perhaps distinguish ownership within the list.

    # Let's refine: show created groups, and then show other groups joined.
    joined_groups_not_created_by_user = request.user.discussion_group_memberships.exclude(creator=request.user).order_by('-created_at')


    context = {
        'dashboard_user': dashboard_user, # The user whose dashboard is being viewed
        'created_groups': created_groups,
        'joined_groups_not_created_by_user': joined_groups_not_created_by_user,
        'all_joined_groups': joined_groups, # For potential use if a combined list is preferred
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
    # Get all groups the user is a member of, excluding those they created to avoid duplication if desired.
    # If you want to list all joined groups including created ones, use: display_user.discussion_group_memberships.all()
    joined_groups_not_created_by_user = display_user.discussion_group_memberships.exclude(creator=display_user).order_by('-created_at')

    context = {
        'display_user': display_user, # The user whose groups are being viewed
        'created_groups': created_groups,
        'joined_groups_not_created_by_user': joined_groups_not_created_by_user,
        'page_title': f"{display_user.first_name or display_user.username}'s Groups"
    }
    return render(request, 'dashboard/my_groups.html', context)
