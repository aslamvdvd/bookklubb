from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserProfileEditForm
# from django.contrib import messages # Will need for edit profile later
# from .forms import UserProfileEditForm # Will need for edit profile later

User = get_user_model()

@login_required
def user_profile_view(request, username):
    """Displays a user's profile information."""
    profile_user = get_object_or_404(User, username=username)
    is_own_profile = (request.user == profile_user)

    context = {
        'profile_user': profile_user,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'accounts/profile_display.html', context)

# Placeholder for edit view, to be developed in Phase 2
# @login_required
# def edit_user_profile_view(request, username):
#     pass

@login_required
def edit_user_profile_view(request, username):
    """Handles editing of a user's profile."""
    user_to_edit = get_object_or_404(User, username=username)

    if request.user != user_to_edit:
        messages.error(request, "You do not have permission to edit this profile.")
        return redirect('accounts:user_profile', username=username)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:user_profile', username=username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileEditForm(instance=user_to_edit)

    context = {
        'form': form,
        'profile_user': user_to_edit
    }
    return render(request, 'accounts/profile_edit.html', context)
