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
            # Form is invalid
            # Check if the only error is the specific empty submission error from forms.py
            is_only_empty_submission_error = False
            if form.non_field_errors() and len(form.non_field_errors()) == 1:
                if "You must provide either text or a file for your message." in form.non_field_errors()[0]:
                    is_only_empty_submission_error = True

            # Only add Django messages (pop-ups) if it's NOT the specific empty submission error
            # or if there are other errors present.
            if not is_only_empty_submission_error:
                for field, errors_list in form.errors.items():
                    for error in errors_list:
                        # Construct a more generic message or use the error as is
                        field_name = field.replace('_', ' ').capitalize() if field != '__all__' else 'Form'
                        django_messages.error(request, f"{field_name}: {error}")
            
            # Fall through to render the page with existing messages and the (invalid) form
            # The template group_chat_interface.html should display form.non_field_errors and field-specific errors.

    # For GET requests or after an invalid POST where we don't redirect, create a fresh form instance if needed
    # However, if POST was invalid, we want to re-render WITH the bound form containing errors.
    # So, form = MessageForm() should only be for GET.
    # The current structure correctly re-uses the bound form for invalid POSTs.
    
    # If it was a POST request and the form was invalid, the `form` variable here is already the bound form with errors.
    # If it was a GET request, we need a new unbound form.
    if request.method == 'GET':
        form = MessageForm()
    # For an invalid POST, `form` is already the bound form from above.

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
