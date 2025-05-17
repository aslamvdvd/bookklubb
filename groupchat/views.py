from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse # JsonResponse for potential AJAX later
from django.conf import settings # Import settings
from django.contrib import messages as django_messages # Alias to avoid conflict with model field
from discussions.models import DiscussionGroup, GroupMembership
from .models import GroupChatMessage
from .forms import MessageForm # Import the new form

@login_required
def group_chat_view(request, group_id):
    """
    Handles displaying the chat interface for a specific group and processing new messages.
    """
    group = get_object_or_404(DiscussionGroup, id=group_id)
    
    try:
        GroupMembership.objects.get(user=request.user, group=group)
    except GroupMembership.DoesNotExist:
        django_messages.error(request, "You are not a member of this group and cannot view its chat.")
        # Consider redirecting to a more appropriate page, like dashboard or group list
        return redirect('dashboard:index', username=request.user.username) 

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.group = group
            try:
                message.save()
                # django_messages.success(request, "Message sent!") # Optional success message
            except Exception as e:
                django_messages.error(request, f"Could not send message: {e}")
            return redirect('groupchat:group_chat_view', group_id=group.id)
        else:
            # Form is invalid, errors will be bound to the form instance
            # We need to pass this form back to the template to display errors
            # For simplicity now, just adding a generic error message. 
            # Proper error display would require passing the form with errors to the context.
            for field, errors in form.errors.items():
                for error in errors:
                    django_messages.error(request, f"{field.capitalize() if field != '__all__' else 'Form'}: {error}")
            # Fall through to render the page with existing messages and the (invalid) form if needed
            # Or, if you prefer a cleaner redirect on error:
            # return redirect('groupchat:group_chat_view', group_id=group.id)

    # For GET requests or after an invalid POST, create a fresh form instance
    form = MessageForm() 

    chat_messages = GroupChatMessage.objects.filter(group=group).select_related('user').order_by('timestamp')
    
    context = {
        'group': group,
        'messages': chat_messages, # Renamed to avoid conflict if 'messages' context processor is used by Django messages
        'form': form, 
        'platform_name': settings.PLATFORM_NAME,
    }
    return render(request, 'groupchat/group_chat_interface.html', context)

# Placeholder view until implementation starts
from django.http import HttpResponse
def placeholder_view(request):
    return HttpResponse("Group chat view placeholder.")
