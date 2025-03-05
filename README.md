# Library Tracking System

## Table of Contents

- [Description](#description)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
- [Accessing the Application](#accessing-the-application)
  - [Django Admin Interface](#django-admin-interface)
  - [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Additional Resources](#additional-resources)

---

## Description

Welcome to the **Library Tracking System**! This project is a comprehensive application built with **Python**, **Django**, **Django REST Framework (DRF)**, and **Celery**. It manages authors, books, members, and loans within a library context. The application is fully containerized using **Docker**, allowing for easy setup and deployment. Whether you're a developer looking to explore the project or setting it up for development purposes, this README will guide you through the necessary steps.

## Technologies Used

- **Python 3.9**
- **Django 4.2**
- **Django REST Framework**
- **Celery 5.3**
- **Redis 6**
- **PostgreSQL 13**
- **Docker & Docker Compose**

## Features

- **Author Management**: Create, read, update, and delete authors.
- **Book Management**: Manage books with genres, ISBNs, and availability status.
- **Member Management**: Handle library members linked to Django user accounts.
- **Loan Management**: Track book loans and returns.
- **API Endpoints**: CRUD operations for all models using Django REST Framework.
- **Asynchronous Tasks**: Celery tasks for sending loan notifications and overdue reminders.
- **Admin Interface**: Django admin panel for data management.
- **Docker-Ready**: Easy setup and deployment using Docker and Docker Compose.

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://gitlab.com/search-atlas-interviews/django-library-tracking-system
   cd django-library-tracking-system  
   
   # If you dont have a prefered version control, we recommend https://github.com/new (free)
   git remote rename origin upstream
   git remote add origin [URL of your newly created repo: https://github.com/...]
   git push -u origin main
   ```

2. **Create a `.env` File**

   In the root directory, create a `.env` file to store environment variables.

   ```bash
   touch .env
   ```

   **Content of `.env`:**

   ```env
   # .env
   DEBUG=1
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   DATABASE_URL=postgres://library_user:library_password@db:5432/library_db
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   SECRET_KEY=your-secret-key
   DEFAULT_FROM_EMAIL=admin@library.com
   ```

   > **Note:** Replace `your-secret-key` with a secure key. Ensure that `.env` is included in `.gitignore` to prevent committing sensitive information.

3. **Build and Run Docker Containers**

   ```bash
   docker-compose build
   docker-compose up
   ```

   This command will:
   - Start PostgreSQL (`db`) and Redis (`redis`) services.
   - Build and run the Django application (`web`).
   - Run the Celery worker (`celery`).

4. **Initialize the Django Project**

   In a separate terminal, apply migrations and create a superuser.

   ```bash
   docker-compose run web python manage.py makemigrations
   docker-compose run web python manage.py migrate
   docker-compose run web python manage.py createsuperuser
   ```

   Follow the prompts to create a superuser account.

### Running the Project

Start all services with Docker Compose:

```bash
docker-compose up
```

**Stopping the Services:**

To stop the running containers, press `CTRL+C` in the terminal where `docker-compose up` is running, then execute:

```bash
docker-compose down
```

## Accessing the Application

### Django Admin Interface

- **URL:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Login:** Use the superuser credentials you created during setup.
- **Functionality:** Manage authors, books, members, and loans through the admin panel.

### API Endpoints

- **Base URL:** [http://localhost:8000/api/](http://localhost:8000/api/)
- **Endpoints:**
  - `/api/authors/`: CRUD operations for authors.
  - `/api/books/`: CRUD operations for books.
  - `/api/members/`: CRUD operations for members.
  - `/api/loans/`: CRUD operations for loans.
- **Access:** Use tools like **Postman**, **cURL**, or the DRF browsable API to interact with the endpoints.

## Project Structure

After following all the setup steps, your project directory (`library-tracking-system/`) should look like this:

```
library-tracking-system/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .gitignore
├── manage.py
├── library_system/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── library/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tasks.py
    ├── tests.py
    └── views.py
```

## Additional Resources

- **Django Documentation:** [https://docs.djangoproject.com/en/4.2/](https://docs.djangoproject.com/en/4.2/)
- **Django REST Framework Documentation:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
- **Celery Documentation:** [https://docs.celeryproject.org/en/stable/](https://docs.celeryproject.org/en/stable/)
- **Docker Documentation:** [https://docs.docker.com/](https://docs.docker.com/)
- **PostgreSQL Documentation:** [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

---

## Troubleshooting

- **Docker Issues:**
  - Ensure Docker and Docker Compose are installed correctly.
  - Check if ports `8000`, `5432`, and `6379` are free or adjust them in `docker-compose.yml`.

- **Environment Variables:**
  - Double-check the `.env` file for correct configurations.
  - Ensure sensitive information like `SECRET_KEY` is set properly.

- **Migrations:**
  - If you encounter migration issues, try resetting the database volumes:
    ```bash
    docker-compose down -v
    docker-compose up --build
    ```

- **Celery Worker Not Running:**
  - Ensure the Celery service is defined correctly in `docker-compose.yml`.
  - Check logs for any errors related to Celery.

---

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

---

Thank you for setting up the **Library Tracking System**! If you have any questions or need further assistance, please reach out to the project maintainer.