from django.http import JsonResponse, HttpResponse

def json_debug_view(request):
    # Returns an empty JSON response or a simple OK for debug-related endpoints
    # to prevent 404s in logs from browser dev tools.
    if request.path.endswith('/version') or request.path.endswith('/list'):
        return JsonResponse({})
    return HttpResponse(status=200) # Generic OK for any other json/ path if needed 