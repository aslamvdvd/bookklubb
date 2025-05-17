# Homepage App

This app is responsible for serving the main landing page of the BookHaven platform. It provides an entry point for both authenticated and unauthenticated users.

## Key Features:

*   **Welcome Message**: Displays a welcoming message and a brief introduction to the platform.
*   **Call to Action**: Encourages new users to register or existing users to log in.
*   **Highlights (Future)**: May showcase featured content, popular discussion groups, or platform news.
*   **Navigation**: Provides primary navigation links to other parts of the site.

## Main Components:

*   `views.py`: Contains the logic to render the homepage.
*   `urls.py`: Defines the URL for the homepage.
*   `templates/homepage/`: Contains the HTML template for the homepage.
*   `static/homepage/`: May contain homepage-specific static files (CSS, JavaScript) if needed, though most styling might be global or from `base.html`. 