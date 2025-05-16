# homepage/context_processors.py

from django.conf import settings

def platform_name(request):
    return {
        'platform_name': settings.PLATFORM_NAME
    }
