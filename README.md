# Task Management API

A production-style RESTful Task Management API built with **Python, Django REST Framework, and PostgreSQL**.

The API provides authenticated users with tools to create and manage tasks, update task status, organize tasks by category and priority, filter and order results, and manage recurring tasks.

## 🌐 Live API

**Base URL:**
https://task-management-api-wpw5.onrender.com/api/

The API is deployed on **Render** and can be used for testing.

## 🚀 Features

* User authentication
* Authenticated task management
* Create, view, update, and delete tasks
* Task status workflow

  * Pending
  * In Progress
  * Completed
  * Cancelled
* Task priority management
* Task categories
* Filtering by task fields
* Ordering and sorting
* Recurring tasks

  * Daily
  * Weekly
  * Monthly
* Automatic handling of completed recurring tasks
* Automated tests
* PostgreSQL database support
* Docker support
* Production deployment with Gunicorn
* Render deployment

## 🛠️ Tech Stack

* **Python**
* **Django**
* **Django REST Framework**
* **PostgreSQL**
* **Docker**
* **Gunicorn**
* **Pytest**
* **Render**

## 🏗️ Project Structure

```text
Task_Management_API/
│
├── accounts/              # User authentication and account functionality
├── Tasks/                 # Task management functionality
├── taskhub/               # Django project configuration
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Local container configuration
├── requirements.txt       # Python dependencies
└── manage.py              # Django management commands
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/otieno-backend/Task_Management_API.git

cd Task_Management_API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## 🔐 Authentication

The API uses token-based authentication.

After authentication, include the token in API requests:

```text
Authorization: Token YOUR_TOKEN
```

Authenticated users can access and manage their tasks according to the application's permissions.

## 📋 Example API Endpoints

| Method    | Endpoint           | Description         |
| --------- | ------------------ | ------------------- |
| POST      | `/api/...`         | User authentication |
| GET       | `/api/tasks/`      | List tasks          |
| POST      | `/api/tasks/`      | Create a task       |
| GET       | `/api/tasks/<id>/` | View a task         |
| PUT/PATCH | `/api/tasks/<id>/` | Update a task       |
| DELETE    | `/api/tasks/<id>/` | Delete a task       |

> Check the project's URL configuration for the complete list of available endpoints.

## 🔎 Task Management

Tasks support several fields and workflows, including:

* Title
* Description
* Status
* Priority
* Category
* Due date
* Recurrence

Supported statuses:

```text
PENDING
IN_PROGRESS
COMPLETED
CANCELLED
```

Supported recurrence options:

```text
NONE
DAILY
WEEKLY
MONTHLY
```

## 🧪 Testing

The project includes automated tests covering important API behavior, including:

* Task creation
* Authentication
* Task status changes
* Task completion
* Recurring task behavior
* Category filtering
* Status filtering
* Priority filtering
* Ordering

Run the test suite with:

```bash
pytest -v
```

## 🐳 Docker

The project includes Docker configuration for running the application in containers.

Build and start the services with:

```bash
docker compose up --build
```

## 🚀 Deployment

The application is deployed on **Render** using Django and Gunicorn.

Production deployment demonstrates experience with:

* Environment configuration
* PostgreSQL
* Gunicorn
* Docker
* Static files
* Production Django settings
* Cloud deployment

## 📚 What I Built

This project demonstrates my experience with:

* Building RESTful APIs with Django REST Framework
* Designing database-backed applications
* Implementing authentication and permissions
* Building task workflows
* Implementing filtering and ordering
* Working with recurring tasks
* Writing automated tests
* Containerizing applications with Docker
* Deploying backend applications
* Debugging and improving production-style applications

## 🔮 Future Improvements

Planned improvements include:

* Redis caching
* Celery background workers
* Nginx
* Improved production monitoring
* Application logging and metrics
* More comprehensive API documentation
* CI/CD with GitHub Actions

## 👨‍💻 Author

**Brian Otieno**

Backend Developer focused on Python, Django, Django REST Framework, PostgreSQL, and REST APIs.

GitHub:
https://github.com/otieno-backend

## ⭐ Project

If you find this project useful, feel free to star the repository.
