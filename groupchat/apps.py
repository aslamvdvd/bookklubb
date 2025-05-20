"""
Application configuration for the groupchat app.

This module defines the configuration class for the groupchat Django application.
"""
from django.apps import AppConfig


class GroupchatConfig(AppConfig):
    """
    Configuration class for the 'groupchat' Django application.

    Sets application-specific settings such as the default auto field
    for models and the application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'groupchat'
