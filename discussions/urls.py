from django.urls import path
from . import views

app_name = 'discussions'  # Crucial for namespacing

urlpatterns = [
    path('create/', views.create_discussion_group, name='create_group'),
    # Future URLs for discussions app can be added here
    # e.g., path('<int:group_id>/', views.group_detail, name='group_detail'),
] 