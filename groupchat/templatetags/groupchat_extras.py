"""
Custom template tags and filters for the groupchat application.

This module provides custom tags and filters to be used within
Django templates related to the groupchat app.
"""
import os
from django import template

register = template.Library()

@register.filter(name='filename_only')
def filename_only(value):
    """
    Returns the base name of a file path (i.e., the part after the last '/').
    Example: 'group_chat_files/2023/05/17/myfile.txt' -> 'myfile.txt'
    """
    if hasattr(value, 'name'): # Handles FileField
        return os.path.basename(value.name)
    elif isinstance(value, str): # Handles string paths
        return os.path.basename(value)
    return value # Return original value if not a known file path type 