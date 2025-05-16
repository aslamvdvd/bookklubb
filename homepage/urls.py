from django.urls import path
from . import views

app_name='homepage'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.auth_view, name='login'),
    path('signup/', views.auth_view, name='signup'),
]
