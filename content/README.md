# Content App

This app manages the various types of content available on the BookHaven platform, such as books, articles, user-generated media, and more.

## Key Features:

*   **Content Modeling**: Defines the structure for different content types (e.g., `Book`, `Article`).
*   **Content Creation & Management**: Allows for the addition, updating, and deletion of content (primarily through the admin interface or future user submission forms).
*   **Content Display**: Provides views and templates for listing and detailing content items.
*   **Categorization/Tagging (Future)**: Will allow content to be organized with categories and tags for better discoverability.
*   **Rating & Reviews (Future)**: Will enable users to rate and review content.

## Main Components:

*   `models.py`: Defines content-related models (e.g., `Genre`, `ContentBase`, `Book`, `UserUploadedContent`).
*   `views.py`: Contains logic for displaying content lists and detail pages.
*   `urls.py`: Maps URLs for content browsing.
*   `admin.py`: Configures how content models are managed in the Django admin. 