from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.contenttypes.models import ContentType # For filtering by content type
from discussions.models import DiscussionGroup
from content.models import ContentItem # To search by content_item.title
from django.contrib.auth import get_user_model
from .forms import DiscussionSearchForm
from django.http import JsonResponse # Added JsonResponse import

User = get_user_model()

def search_discussions_view(request):
    """
    Handles searching and filtering for discussion groups.
    """
    form = DiscussionSearchForm(request.GET or None)
    results = DiscussionGroup.objects.all().select_related('creator', 'content_item') # Start with all, then filter
    query = None
    applied_filters = {}

    if form.is_valid():
        query = form.cleaned_data.get('query')
        is_private_filter = form.cleaned_data.get('is_private')
        content_type_filter = form.cleaned_data.get('content_type')
        ordering = form.cleaned_data.get('ordering', '-created_at') # Default ordering

        if query:
            name_desc_q = Q(name__icontains=query) | Q(description__icontains=query)
            creator_q = (
                Q(creator__username__icontains=query) |
                Q(creator__first_name__icontains=query) |
                Q(creator__last_name__icontains=query)
            )
            content_focus_q = Q(content_item__title__icontains=query)
            combined_search_q = name_desc_q | creator_q | content_focus_q
            results = results.filter(combined_search_q)
            applied_filters['query'] = query

        if is_private_filter:
            results = results.filter(is_private=(is_private_filter == 'true'))
            applied_filters['is_private'] = is_private_filter
        
        if content_type_filter: # content_type_filter will be model name string e.g. 'book'
            try:
                # Find the ContentType object for the model name
                # This assumes model names in CONTENT_TYPE_CHOICES are lowercase model names
                actual_content_type_obj = ContentType.objects.get(model=content_type_filter.lower())
                # Filter DiscussionGroup by the content_type of their related content_item
                results = results.filter(content_item__polymorphic_ctype=actual_content_type_obj)
                applied_filters['content_type'] = content_type_filter
            except ContentType.DoesNotExist:
                # Handle case where content_type_filter string doesn't match a real ContentType
                # For instance, if CONTENT_TYPE_CHOICES generation had an issue or input was tampered
                pass # Or add a message, or log an error

        if ordering:
            if ordering == '-members_count': # Example for a custom ordering needing annotation
                results = results.annotate(members_count=Count('members')).order_by('-members_count', '-created_at')
            elif ordering in ['name', '-name', 'created_at', '-created_at']:
                results = results.order_by(ordering)
            applied_filters['ordering'] = ordering
        else: # Default ordering if none specified or invalid
            results = results.order_by('-created_at')
            applied_filters['ordering'] = '-created_at'
        
        results = results.distinct() # Ensure distinct results after all filtering

        # Exclude groups created by the current user
        if request.user.is_authenticated:
            results = results.exclude(creator=request.user)

    else: # If form is not valid (e.g., on initial page load without GET params)
        # Apply default ordering for initial load if no specific ordering is requested
        ordering_param = request.GET.get('ordering', '-created_at')
        if ordering_param in ['name', '-name', 'created_at', '-created_at']:
             results = results.order_by(ordering_param)
        else:
            results = results.order_by('-created_at')
        applied_filters['ordering'] = ordering_param if ordering_param in ['name', '-name', 'created_at', '-created_at'] else '-created_at'
        # results = DiscussionGroup.objects.none() # Or show all/popular if form is not submitted

    context = {
        'form': form, # Pass the form with current GET data to repopulate fields
        'results': results,
        'query': request.GET.get('query'), # Pass original query for display
        'applied_filters': applied_filters, # Pass applied filters for display/state
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
