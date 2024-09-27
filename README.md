# Django Online Shop

Welcome to the Django Online Shop! This project is a full-featured e-commerce platform built with Django and Django REST Framework (DRF). It includes user authentication, product management, shopping cart functionality, order processing, and more. Additionally, the project is integrated with Celery for asynchronous task management.

## Features

- User Registration and Authentication (JWT-based)
- Product Listings and Categories
- Shopping Cart and Checkout System
- Order Management
- Task Scheduling with Celery and Django Celery Beat
- Asynchronous Email Notifications
- High level performance of load testing
- API Documentation with Swagger and Redoc
- Secure Authentication using djangorestframework-simplejwt
- Flexible filtering using django-filter
- Custom manage.py commands to create random and fake data for using during the development.
- Custom Logging middleware (see middlewares/logger.py).
- Custom additional Password hasher (see hashers.py). 

## Technologies Used
- **Django** 4.2 - High-level Python web framework for rapid development.
- **Django REST Framework (DRF)** 3.15.2 - Toolkit for building Web APIs.
- **Celery** 5.4.0 - Distributed task queue for handling background processes.
- **Django Celery Beat** 2.7.0 - Scheduler for periodic tasks in Celery.
- **djangorestframework-simplejwt** 5.3.1 - JWT authentication for Django REST Framework.
- **drf-yasg** 1.21.7 - Swagger/OpenAPI documentation generator for Django REST Framework.
- **django-mail-templated** 2.6.5 - Email templating for Django.
- **djoser** 2.2.3 - Authentication third-party package that has been used in second version of authentication API (users app).
- **django-filter** 24.3 - Advanced filtering for Django REST Framework.
- **Faker** 28.1.0 - Generating random test data for development and testing.
- **Pillow** 10.4.0 - Image processing library for handling image uploads.
- **Locust** Load testing framework to handle the load testing.

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HosseinSiw/django-online-shop.git
   cd django-online-shop

2. Run the project using docker compose:
    ```bash
    docker compose up

3. Navigate to your localhost via your browser and open your desired documentation page, and test my developed APIs.
   ```url
   Swagger: http://localhost:8000/swagger/
   Redoc: http://localhost:8000/redoc/
