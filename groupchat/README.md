# Group Chat App (`groupchat`)

This Django app provides the real-time chat functionality for discussion groups within the BookHaven platform.

## Features

-   In-group text messaging.
-   File attachments in messages.
-   Chat bubble interface.
-   Admin roles for group creators (and designated users).

## Models

-   `GroupChatMessage`: Stores individual messages, linking to the user, group, and containing text or file content.

## Future Considerations

-   Real-time updates via WebSockets (e.g., Django Channels).
-   Message reply threads.
-   Editing/deleting messages (with permissions).
-   User online status indicators.
-   Read receipts. 