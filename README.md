# Task Management API

The API enables users to manage tasks, organize them into categories, track completion status, and automate recurring tasks.

## 🚀 Live API

https://task-management-api-wpw5.onrender.com

## 📂 GitHub Repository

https://github.com/otieno-backend/Task_Management_API

---

# Features

## Authentication

* User Registration
* User Login
* User Logout
* Token-Based Authentication
* Protected Endpoints

## User Roles

* Admin Dashboard Access
* Regular User Dashboard Access
* Custom Role-Based Permissions

## Task Management

* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Mark Tasks as Complete
* Task Categories
* Task Priorities
* Due Dates
* Task Status Tracking

## Recurring Tasks

Supports:

* Daily Recurrence
* Weekly Recurrence
* Monthly Recurrence

When a recurring task is marked as completed, the next occurrence is automatically generated.

## Filtering & Sorting

Filter tasks by:

* Status
* Priority
* Due Date
* Category

Sort tasks by:

* Due Date (Ascending/Descending)
* Priority (Ascending/Descending)

## Pagination

Task results are paginated for improved performance and scalability.

---

# Technology Stack

## Backend

* Python
* Django
* Django REST Framework

## Authentication

* DRF Token Authentication

## Database

* SQLite (Development)
* PostgreSQL (Production Ready)

# Base URL

## Local Development

```text
http://127.0.0.1:8000/api/
```

## Production

```text
https://task-management-api-wpw5.onrender.com/api/
```

---

# Authentication Endpoints

## Register User

### POST

```http
/api/register/
```

### Request Body

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

### Response

```json
{
  "message": "User created successfully",
  "token": "your-token",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com"
  }
}
```

---

## Login

### POST

```http
/api/login/
```

### Request

```json
{
  "username": "john",
  "password": "password123"
}
```

---

## Logout

### POST

```http
/api/logout/
```

Authentication Required

---

# Dashboard Endpoints

## Admin Dashboard

### GET

```http
/api/admin/dashboard/
```

Requires:

* Authenticated User
* Admin Role

---

## User Dashboard

### GET

```http
/api/user/dashboard/
```

Requires:

* Authenticated User
* Regular User Role

---

# Task Endpoints

## Get All Tasks

### GET

```http
/api/tasks/
```

---

## Create Task

### POST

```http
/api/tasks/
```

Example:

```json
{
  "title": "Finish API Project",
  "description": "Complete backend implementation",
  "priority": "HIGH",
  "due_date": "2026-06-15T12:00:00Z",
  "recurrence": "DAILY"
}
```

---

## Retrieve Single Task

### GET

```http
/api/tasks/{id}/
```

---

## Update Task

### PUT

```http
/api/tasks/{id}/
```

or

### PATCH

```http
/api/tasks/{id}/
```

---

## Delete Task

### DELETE

```http
/api/tasks/{id}/
```

---

## Complete Task

### PATCH

```http
/api/tasks/{id}/complete/
```

Behavior:

* Marks task as completed.
* Records completion timestamp.
* Automatically creates the next task if recurrence is enabled.

---

# Task Filters

## Status

```http
/api/tasks/?status=PENDING
```

## Priority

```http
/api/tasks/?priority=HIGH
```

## Due Date

```http
/api/tasks/?due_date=2026-06-15
```

## Category Name

```http
/api/tasks/?category=Work
```

## Category ID

```http
/api/tasks/?category=1
```

---

# Task Ordering

## Due Date Ascending

```http
/api/tasks/?ordering=due_date
```

## Due Date Descending

```http
/api/tasks/?ordering=-due_date
```

## Priority Ascending

```http
/api/tasks/?ordering=priority
```

## Priority Descending

```http
/api/tasks/?ordering=-priority
```

---

# Category Endpoints

## Get Categories

### GET

```http
/api/categories/
```

---

## Create Category

### POST

```http
/api/categories/
```

---

## Retrieve Category

### GET

```http
/api/categories/{id}/
```

---

## Update Category

### PUT/PATCH

```http
/api/categories/{id}/
```

---

## Delete Category

### DELETE

```http
/api/categories/{id}/
```

---

# Authentication Header

Include your token in every protected request:

```http
Authorization: Token your_token_here
```

Example:

```http
Authorization: Token 123abc456def789
```

---

# Project Structure

```text
Task_Management_API/

├── accounts/
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   └── urls.py
│
├── Tasks/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── pagination.py
│   └── urls.py
│
├── project/
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

# Security

* Token Authentication
* User-Specific Task Access
* Role-Based Permissions
* Protected API Endpoints

---

# Future Improvements

* JWT Authentication
* Email Notifications
* Task Reminders
* Search Functionality
* Team Collaboration
* Task Attachments
* Swagger/OpenAPI Documentation

---

# Author

Otieno Backend

GitHub:
https://github.com/otieno-backend

---

# License

This project is licensed under the MIT License.
