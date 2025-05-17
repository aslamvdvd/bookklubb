# BookHaven: Your Digital Content and Community Hub

BookHaven is a comprehensive Django-based web platform designed to bring together content enthusiasts. It offers a space for users to discover, share, and discuss various media types, participate in user-led discussion groups, and manage their digital literary life.

## Features

*   **User Authentication**: Secure registration, login, and logout functionality. Custom user model to store detailed user information.
*   **Content Marketplace/Hub**: A place for users to explore and (conceptually) share diverse content (books, articles, etc.).
*   **Discussion Groups**: Users can create, join, and participate in topic-focused discussion groups.
*   **User Dashboards**: Personalized landing pages for users, showcasing their activity, recommendations, and providing easy navigation.
*   **AI Facilitator (Conceptual)**: Future integration planned for an AI to facilitate discussions and provide recommendations.
*   **Homepage**: Engaging landing page for both new and returning users.
*   **Static Asset Management**: Organized handling of CSS, JavaScript, and images.
*   **Environment-based Configuration**: Secure and flexible settings management using `.env` files.

## Technology Stack

*   **Backend**: Python, Django
*   **Database**: PostgreSQL (configured, can be swapped)
*   **Frontend**: HTML, Tailwind CSS, JavaScript
*   **Environment Management**: `python-dotenv`

## Project Structure

The project is organized into several Django apps:

*   `bookhaven/`: Main project configuration directory.
*   `accounts/`: Manages user accounts, profiles, and authentication.
*   `content/`: Handles the creation, management, and display of various content types.
*   `dashboard/`: Provides user-specific dashboards and interfaces.
*   `discussions/`: Manages discussion groups, posts, and interactions.
*   `homepage/`: Serves the main landing page of the platform.
*   `static/`: Project-level static files (CSS, JS, images).
*   `templates/`: Base templates and project-level templates.

## Setup and Installation

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd BookHaven # Or your project's root directory name
    ```

2.  **Create and Activate a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be generated and maintained. If it doesn't exist, you'll need to create one based on project dependencies like Django, psycopg2-binary, python-dotenv, etc.)*

4.  **Set Up Environment Variables**:
    Create a `.env` file in the project root (alongside `manage.py`). Add the following, replacing placeholder values with your actual configuration:
    ```env
    DEBUG=True
    SECRET_KEY=your_very_secret_and_unique_django_secret_key # Keep this safe!
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost # Or your DB host
    DB_PORT=5432      # Or your DB port

    PLATFORM_NAME="BookHaven"
    PLATFORM_FIRST_NAME="Book"
    PLATFORM_LAST_NAME="Haven"
    ```

5.  **Apply Database Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a Superuser (Optional, for Admin Access)**:
    ```bash
    python manage.py createsuperuser
    ```

## Running the Development Server

Once the setup is complete, you can run the Django development server:

```bash
python manage.py runserver
```

The application will typically be available at `http://127.0.0.1:8000/`.

## Next Steps

*   Implement detailed functionality for each app.
*   Develop the AI Facilitator features.
*   Write comprehensive tests.
*   Refine UI/UX based on user feedback. 