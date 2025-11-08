from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse # Import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError # Import IntegrityError
from .forms import DiscussionGroupForm
from .models import DiscussionGroup, GroupMembership # Ensure GroupMembership is imported
import logging # Import logging

logger = logging.getLogger(__name__) # Get a logger instance

# Create your views here.

@login_required
def create_discussion_group(request):
    """
    Handles the creation of a new discussion group.
    Assigns the creator as an admin in the GroupMembership table.
    """
    logger.info(f"[CREATE_GROUP_START] User: {request.user.username} (ID: {request.user.id}), Authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        form = DiscussionGroupForm(request.POST)
        logger.info(f"[CREATE_GROUP_POST] User: {request.user.username} (ID: {request.user.id}), Form received.")
        if form.is_valid():
            logger.info(f"[CREATE_GROUP_VALID_FORM] User: {request.user.username} (ID: {request.user.id}), Form is valid.")
            group = form.save(commit=False)
            
            logger.info(f"[CREATE_GROUP_ASSIGN_CREATOR] Current request.user: {request.user.username} (ID: {request.user.id})")
            group.creator = request.user
            logger.info(f"[CREATE_GROUP_POST_ASSIGN_CREATOR] group.creator temporarily set to: {group.creator.username} (ID: {group.creator.id}) if group.creator else None")
            
            try:
                group.save() # Database save for DiscussionGroup instance
                logger.info(f"[CREATE_GROUP_SAVED] Group '{group.name}' saved. DB Creator: {group.creator.username} (ID: {group.creator.id})")
                
                # Now that the group is saved and has an ID, create the GroupMembership for the creator
                GroupMembership.objects.create(
                    user=request.user,
                    group=group,
                    role=GroupMembership.ROLE_ADMIN # Assign admin role
                )
                logger.info(f"[CREATE_GROUP_ADMIN_ASSIGNED] User {request.user.username} assigned as ADMIN for group '{group.name}'.")

            except IntegrityError as ie:
                # Check if it's our specific unique_group_name_per_creator constraint
                # This check might need to be more robust depending on the DB error message specifics
                if 'unique_group_name_per_creator' in str(ie).lower() or (hasattr(ie, 'args') and any('unique_group_name_per_creator' in str(arg).lower() for arg in ie.args)):
                    messages.error(request, "Group with this name already exists in your account.")
                    # Pass the form back with existing data, but not explicitly marking fields as erroneous
                    # The error is a general form error here due to the unique constraint, not a field-specific one.
                    return render(request, 'discussions/create_group.html', {'form': form})
                else:
                    # It's some other IntegrityError
                    logger.error(f"[CREATE_GROUP_INTEGRITY_ERROR] Unhandled IntegrityError: {ie}. request.user was {request.user.username}")
                    messages.error(request, "A database integrity error occurred. Please try again.")
                    return render(request, 'discussions/create_group.html', {'form': form})
            except Exception as e:
                logger.error(f"[CREATE_GROUP_SAVE_ERROR_OR_MEMBERSHIP] Error saving group or creating admin membership: {e}. request.user was {request.user.username}")
                messages.error(request, "Could not save the group or assign admin role due to a server error.")
                # It might be prudent to delete the group if membership creation fails to avoid orphaned groups
                # if group.id: group.delete()
                return render(request, 'discussions/create_group.html', {'form': form})
            
            # The line `group.members.add(request.user)` is no longer needed as membership is handled by GroupMembership.objects.create above.
            # logger.info(f"[CREATE_GROUP_MEMBERS_ADDED] User {request.user.username} added to members of group '{group.name}'.")
            
            messages.success(request, f'Discussion group "{group.name}" created successfully!')
            
            try:
                redirect_url = reverse('dashboard:index', kwargs={'username': request.user.username})
                logger.info(f"[CREATE_GROUP_REDIRECT] Attempting to redirect to (using reverse): {redirect_url} for user {request.user.username}")
                return redirect(redirect_url)
            except Exception as e:
                logger.error(f"[CREATE_GROUP_REDIRECT_ERROR] Error reversing dashboard:index for user {request.user.username}: {e}")
                # Consider a more user-friendly fallback, perhaps to a generic dashboard or the group list if available
                return redirect('/') 

        else:
            error_log_message = f"[CREATE_GROUP_INVALID_FORM] Form errors: {form.errors.as_json()} for user {request.user.username}"
            logger.error(error_log_message)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DiscussionGroupForm()
    
    return render(request, 'discussions/create_group.html', {'form': form})

@login_required
def join_group_view(request, group_id):
    """Allows a logged-in user to join a public discussion group."""
    group = get_object_or_404(DiscussionGroup, id=group_id)

    if group.is_private:
        messages.error(request, "This group is private and cannot be joined directly.")
        return redirect('search_hub:discussion_search_results') # Or wherever appropriate

    # Check if already a member
    if group.members.filter(id=request.user.id).exists():
        messages.info(request, f"You are already a member of \"{group.name}\".")
        return redirect('groupchat:group_chat_view', group_id=group.id)

    try:
        GroupMembership.objects.create(
            user=request.user,
            group=group,
            role=GroupMembership.ROLE_MEMBER
        )
        messages.success(request, f"Successfully joined \"{group.name}\"!")
        return redirect('groupchat:group_chat_view', group_id=group.id)
    except Exception as e:
        logger.error(f"[JOIN_GROUP_ERROR] User {request.user.username} failed to join group {group.id}: {e}")
        messages.error(request, "Could not join the group due to a server error.")
        return redirect('search_hub:discussion_search_results')
