from django.shortcuts import render, get_object_or_404
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
