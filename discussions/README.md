# Discussions App

This app facilitates user interaction and community building through discussion groups on the BookHaven platform.

## Key Features:

*   **Group Creation**: Allows users to create new discussion groups based on topics of interest.
*   **Group Discovery/Search**: Enables users to find and join existing groups.
*   **Posting and Commenting**: Users can create posts within groups and comment on them.
*   **Membership Management**: Handles user membership within groups.
*   **Moderation (Future)**: Will provide tools for group owners/moderators to manage discussions.
*   **AI Facilitator Integration (Future)**: Planned integration for an AI to assist in discussions.

## Main Components:

*   `models.py`: Defines models for `DiscussionGroup`, `Post`, `Comment`, and group memberships.
*   `views.py`: Contains the logic for creating, listing, viewing, and interacting with discussion groups and their content.
*   `forms.py`: Includes forms for creating groups, posts, and comments.
*   `urls.py`: Maps URLs for discussion-related actions.
*   `admin.py`: Configures how discussion models are managed in the Django admin. 