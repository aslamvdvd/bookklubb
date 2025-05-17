from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from accounts.forms import CustomUserCreationForm

# Create your views here.


def index(request):
    context ={
        'platform_name': settings.PLATFORM_NAME,
        'platform_first_name': settings.PLATFORM_FIRST_NAME,
        'platform_last_name': settings.PLATFORM_LAST_NAME,
        'current_year': datetime.now().year
    }
    return render(request, 'homepage/index.html', context)


def login_view(request):
    context = {
        'current_year': datetime.now().year,
        'platform_name': settings.PLATFORM_NAME,
        'form_type': 'login'
    }
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage:index')
            else:
                context['error_message'] = 'Invalid username or password.'
        else:
            context['error_message'] = 'Invalid username or password.'
        context['form'] = form
    else:
        form = AuthenticationForm()
        context['form'] = form
    return render(request, 'homepage/auth.html', context)


def signup_view(request):
    context = {
        'current_year': datetime.now().year,
        'platform_name': settings.PLATFORM_NAME,
        'form_type': 'signup'
    }
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage:index')
        else:
            context['form'] = form
    else:
        form = CustomUserCreationForm()
        context['form'] = form
    return render(request, 'homepage/auth.html', context)