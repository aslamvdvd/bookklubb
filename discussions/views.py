from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse # Import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DiscussionGroupForm
from .models import DiscussionGroup
import logging # Import logging

logger = logging.getLogger(__name__) # Get a logger instance

# Create your views here.

@login_required
def create_discussion_group(request):
    """Handles the creation of a new discussion group."""
    logger.info(f"[CREATE_GROUP_START] User: {request.user.username} (ID: {request.user.id}), Authenticated: {request.user.is_authenticated}")
    if request.method == 'POST':
        form = DiscussionGroupForm(request.POST)
        logger.info(f"[CREATE_GROUP_POST] User: {request.user.username} (ID: {request.user.id}), Form received.")
        if form.is_valid():
            logger.info(f"[CREATE_GROUP_VALID_FORM] User: {request.user.username} (ID: {request.user.id}), Form is valid.")
            group = form.save(commit=False)
            
            # Critical logging before assigning creator
            logger.info(f"[CREATE_GROUP_ASSIGN_CREATOR] Current request.user: {request.user.username} (ID: {request.user.id})")
            group.creator = request.user
            logger.info(f"[CREATE_GROUP_POST_ASSIGN_CREATOR] group.creator temporarily set to: {group.creator.username} (ID: {group.creator.id}) if group.creator else None")
            
            try:
                group.save() # Database save
                logger.info(f"[CREATE_GROUP_SAVED] Group '{group.name}' saved. DB Creator: {group.creator.username} (ID: {group.creator.id})")
            except Exception as e:
                logger.error(f"[CREATE_GROUP_SAVE_ERROR] Error saving group: {e}. request.user was {request.user.username}")
                messages.error(request, "Could not save the group due to a server error.")
                return render(request, 'discussions/create_group.html', {'form': form})

            group.members.add(request.user)
            logger.info(f"[CREATE_GROUP_MEMBERS_ADDED] User {request.user.username} added to members of group '{group.name}'.")
            messages.success(request, f'Discussion group "{group.name}" created successfully!')
            
            try:
                redirect_url = reverse('dashboard:index', kwargs={'username': request.user.username})
                logger.info(f"[CREATE_GROUP_REDIRECT] Attempting to redirect to (using reverse): {redirect_url} for user {request.user.username}")
                return redirect(redirect_url)
            except Exception as e:
                logger.error(f"[CREATE_GROUP_REDIRECT_ERROR] Error reversing dashboard:index for user {request.user.username}: {e}")
                return redirect('/')

        else:
            error_log_message = f"[CREATE_GROUP_INVALID_FORM] Form errors: {form.errors.as_json()} for user {request.user.username}"
            logger.error(error_log_message)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DiscussionGroupForm()
    
    return render(request, 'discussions/create_group.html', {'form': form})
