from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime

# Create your views here.


def index(request):
    context ={
        'platform_name': settings.PLATFORM_NAME,
        'platform_first_name': settings.PLATFORM_FIRST_NAME,
        'platform_last_name': settings.PLATFORM_LAST_NAME,
        'current_year': datetime.now().year
    }
    return render(request, 'homepage/index.html', context)



# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('/')
#     else:
#         form = UserCreationForm()
#     return render(request, 'homepage/signup.html', {'form': form})


def auth_view(request):
    context = {
        'current_year':datetime.now().year,
        'platform_name':settings.PLATFORM_NAME
    }
    if request.resolver_match.url_name == 'login':
        context['form_type'] = 'login'
    elif request.resolver_match.url_name == 'signup':
        context['form_type'] = 'signup'
    
    return render(request, 'homepage/auth.html', context)