from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_index, name='index'),
    path('settings/', views.dashboard_settings_view, name='dashboard_settings'),
    path('my-groups/', views.user_groups_view, name='user_groups'),
] 