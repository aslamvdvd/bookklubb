"""
URL configuration for bookhaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from homepage import views as homepage_views
from bookhaven import views as project_views # Import the new views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Dummy endpoints to silence browser dev tool requests
    path('json/version', project_views.json_debug_view, name='json_version'),
    path('json/list', project_views.json_debug_view, name='json_list'),
    path('login/', homepage_views.login_view, name='login'),
    path('signup/', homepage_views.signup_view, name='signup'),
    path('logout/', homepage_views.logout_view, name='logout'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('discussions/', include('discussions.urls', namespace='discussions')),
    path('search/', include('search_hub.urls', namespace='search_hub')),
    path('groupchat/', include('groupchat.urls', namespace='groupchat')),
    path('<str:username>/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('', include('homepage.urls', namespace='homepage')),
]


# if settings.DEBUG:
#     from django.conf import settings # Ensure settings is imported for below
#     from django.conf.urls.static import static # Ensure static is imported for below
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

