from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def dashboard_index(request, username):
    dashboard_user = get_object_or_404(User, username=username)
    context = {
        'dashboard_user': dashboard_user,
    }
    return render(request, 'dashboard/index.html', context)
