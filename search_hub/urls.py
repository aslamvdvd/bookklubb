from django.urls import path
from . import views

app_name = 'search_hub'

urlpatterns = [
    path('', views.search_discussions_view, name='discussion_search_results'),
    path('api/dynamic-group-search/', views.dynamic_discussion_search_api, name='dynamic_group_search_api'),
    # Future: path('api/dynamic-search/', views.dynamic_search_api, name='dynamic_search_api'),
] 