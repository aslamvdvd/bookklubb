from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse # Import JsonResponse
from discussions.models import DiscussionGroup
from content.models import ContentItem # To search by content_item.title
from django.contrib.auth import get_user_model
from .forms import DiscussionSearchForm
import json # For parsing request body if it were POST JSON, not needed for GET

User = get_user_model()

def search_discussions_view(request):
    """
    Handles searching for discussion groups based on a query for the main results page.
    Searches group name, description, creator's username/name, and content item title.
    """
    form = DiscussionSearchForm(request.GET or None)
    results = DiscussionGroup.objects.none()
    query = None

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            name_desc_q = Q(name__icontains=query) | Q(description__icontains=query)
            creator_q = (
                Q(creator__username__icontains=query) |
                Q(creator__first_name__icontains=query) |
                Q(creator__last_name__icontains=query)
            )
            content_focus_q = Q(content_item__title__icontains=query)
            combined_q = name_desc_q | creator_q | content_focus_q
            results = DiscussionGroup.objects.filter(combined_q).distinct().select_related('creator', 'content_item').order_by('-created_at')
    
    context = {
        'form': form,
        'results': results,
        'query': query,
    }
    return render(request, 'search_hub/search_results.html', context)

def dynamic_discussion_search_api(request):
    """
    API endpoint for dynamic (live) search of discussion groups.
    Returns a JSON response with a limited number of matching groups.
    """
    query = request.GET.get('query', None)
    data = {
        'groups': [],
        'query': query
    }

    if query and len(query) > 1: # Start searching after 1 character
        name_desc_q = Q(name__icontains=query) | Q(description__icontains=query)
        creator_q = (
            Q(creator__username__icontains=query) |
            Q(creator__first_name__icontains=query) |
            Q(creator__last_name__icontains=query)
        )
        content_focus_q = Q(content_item__title__icontains=query)
        combined_q = name_desc_q | creator_q | content_focus_q
        
        # Limit results for dynamic search, select related for efficiency
        # Add .distinct() to avoid duplicate results if a query matches multiple fields in the same group
        groups = DiscussionGroup.objects.filter(combined_q).select_related('creator', 'content_item').distinct().order_by('-created_at')[:10] 
        
        for group in groups:
            data['groups'].append({
                'id': group.pk,
                'name': group.name,
                'description': group.description[:100] + '...' if group.description and len(group.description) > 100 else group.description,
                'creator_username': group.creator.username if group.creator else 'N/A',
                'content_focus_title': group.content_item.title if group.content_item else 'N/A',
                # 'url': reverse('discussions:group_detail', kwargs={'group_id': group.pk}) # Future group detail URL
                'url': '#' # Placeholder for now
            })
            
    return JsonResponse(data)
