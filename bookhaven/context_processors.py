import os

def platform_name(request):
    return {'platform_name': os.getenv('platform_name', 'BookHaven')}