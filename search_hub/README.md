# Search Hub App

This app provides comprehensive search functionalities for the BookHaven platform, allowing users to find discussion groups and potentially other content types based on various criteria.

## Key Features:

*   **Discussion Group Search**: Enables users to search for discussion groups by name, creator (username, first/last name), and focused content item.
*   **Dedicated Search Results Page**: Displays search results in a clear and filterable format.
*   **Dynamic Search API (Future)**: Will provide an endpoint for live search suggestions within a modal or search bar.
*   **Advanced Filtering (Future)**: Will allow users to refine search results based on multiple criteria.

## Main Components:

*   `views.py`: Contains logic for handling search queries, interacting with the database, and rendering results.
*   `forms.py`: Defines search forms.
*   `urls.py`: Maps URLs for search-related views and APIs.
*   `templates/search_hub/`: Contains HTML templates for search interfaces and results display.
*   `static/search_hub/`: Will hold search-specific static files (CSS, JavaScript) for features like the dynamic search modal. 