# Accounts App

This app is responsible for managing user authentication, registration, profiles, and related functionalities within the BookHaven platform.

## Key Features:

*   **User Registration**: Allows new users to create an account.
*   **Login/Logout**: Secure user login and logout mechanisms.
*   **Custom User Model (`CustomUser`)**: Extends the base Django user model to include additional fields like date of birth, bio, etc.
*   **User Profile Management (Future)**: Will allow users to view and edit their profile information.
*   **Password Management (Future)**: Will include password reset and change functionalities.

## Main Components:

*   `models.py`: Defines the `CustomUser` model and `CustomUserManager`.
*   `views.py`: Contains the logic for registration, login, logout, and profile views.
*   `forms.py`: Includes forms for user registration and login.
*   `urls.py`: Maps URLs to their respective views within the app.
*   `admin.py`: Configures how the `CustomUser` model is displayed in the Django admin interface. 