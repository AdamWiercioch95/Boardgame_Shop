# Boardgame Shop

## Introduction
Boardgame Shop is a web application designed to manage a board game store. This project is built using Django and styled with Bootstrap.

## Features Included

- Custom Admin Dashboard
- Search Functionality
- Shopping Cart:
- Order Management
- User Authentication
- Product Reviews and Ratings

## Prerequisites
- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- Virtual environment (optional, but recommended)
- Django 5.0.6 or higher

## How to Run the Project?

### 1. Clone repository & install packages
1. Clone the repository:
    ```bash
    git clone https://github.com/AdamWiercioch95/Boardgame_Shop.git
    cd Boardgame_Shop
    poetry install
    ```

### 2. Open the Project
1. Open your project in your preferred code editor.

### 3. Apply Database Migrations
1. Apply the necessary database migrations:
    ```bash
    python manage.py migrate
    ```

### 4. Run the Development Server
1. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

### 5. Open the Application
1. Open your browser and go to `http://localhost:8000` to see the running application.

## Testing

### 1. Run Tests
1. Use pytest to run the tests:
    ```bash
    pytest <app_name>/tests.py
    ```

## Useful Links
- [Django Documentation](https://docs.djangoproject.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---