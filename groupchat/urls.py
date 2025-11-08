"""
URLS patterns for the group chat application.

This module maps URLs to their corresponding views within the groupchat app.
"""
from django.urls import path
from . import views

app_name = 'groupchat'

urlpatterns = [
    path('group/<int:group_id>/chat/', views.group_chat_view, name='group_chat_view'),
] 