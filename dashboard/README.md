# Dashboard App

This app provides logged-in users with a personalized dashboard, serving as their central hub within the BookHaven platform.

## Key Features:

*   **Personalized Welcome**: Greets the user and provides a quick overview.
*   **Activity Feed (Future)**: Will display recent user activity, such as joined discussions, viewed content, or new messages.
*   **Recommendations (Future)**: Will offer personalized content or group suggestions.
*   **Quick Access Links**: Provides easy navigation to key areas like profile management, discussion group creation/search, and content discovery.

## Main Components:

*   `views.py`: Contains the logic to render the dashboard page, fetching user-specific data.
*   `urls.py`: Defines the URL for accessing the user dashboard.
*   `templates/dashboard/`: Contains the HTML template for the dashboard interface.
*   `static/dashboard/`: Contains dashboard-specific static files (CSS, JavaScript). 