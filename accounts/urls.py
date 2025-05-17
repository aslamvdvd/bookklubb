from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Example: /accounts/profile/testuser/
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    # Example: /accounts/profile/testuser/edit/
    path('profile/<str:username>/edit/', views.edit_user_profile_view, name='edit_user_profile'),
    # Add other account-related URLs here later (e.g., password_change)
] 