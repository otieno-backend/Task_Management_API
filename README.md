# 📌 Task Management API

A scalable RESTful API for managing tasks, categories, and recurring workflows with authentication, filtering, role-based access control, and full Docker support.

---

## 🚀 Live API

👉 [https://task-management-api-wpw5.onrender.com](https://task-management-api-wpw5.onrender.com)

---

## 📂 Repository

👉 [https://github.com/otieno-backend/Task_Management_API](https://github.com/otieno-backend/Task_Management_API)

---

# ✨ Features

## 🔐 Authentication

* User Registration
* Login / Logout
* Token-Based Authentication (DRF Token Auth)
* Protected Endpoints

---

## 👥 User Roles

* Admin Dashboard Access
* Regular User Dashboard Access
* Role-Based Permissions

---

## 📝 Task Management

* Create, Read, Update, Delete Tasks
* Mark Tasks as Complete
* Task Categories
* Priority Levels
* Due Dates
* Status Tracking

---

## 🔁 Recurring Tasks

Supports automatic task regeneration for:

* Daily recurrence
* Weekly recurrence
* Monthly recurrence

✔ Completed recurring tasks automatically generate the next instance.

---

## 🔍 Filtering & Sorting

### Filters

* Status
* Priority
* Due Date
* Category (by name or ID)

### Sorting

* Due date (ascending/descending)
* Priority (ascending/descending)

---

## 📄 Pagination

Efficient paginated responses for scalable performance.

---

# 🛠 Tech Stack

## Backend

* Python
* Django
* Django REST Framework

## Authentication

* DRF Token Authentication

## Database

* SQLite (development)
* PostgreSQL (production-ready)

## DevOps

* Docker
* Docker Compose
* Gunicorn

---

# 🌐 API Base URL

## Local (Docker)

```text id="k7q1lz"
http://localhost:8000/api/
```

## Production

```text id="x1v9wp"
https://task-management-api-wpw5.onrender.com/api/
```

---

# 🐳 Docker Deployment

This project is fully containerized using Docker and Docker Compose.

## 📦 Prerequisites

* Docker
* Docker Compose

---

## 🚀 Run the Project

### 1. Clone repository

```bash id="g3nq9a"
git clone https://github.com/otieno-backend/Task_Management_API.git
cd Task_Management_API
```

---

### 2. Build and start containers

```bash id="p8m2ld"
docker compose up --build
```

---

### 3. Run in background

```bash id="w7k3vd"
docker compose up -d
```

---

### 4. Apply migrations

```bash id="n4x8qp"
docker compose exec web python manage.py migrate
```

---

### 5. Create superuser

```bash id="t6m1ax"
docker compose exec web python manage.py createsuperuser
```

---

## 🌍 Access API

```text id="c9v2ld"
http://localhost:8000/api/
```

---

## 🧱 Docker Services

### 🟦 Web (Django + Gunicorn)

* Runs Django API
* Exposed on port 8000

### 🟩 Database (PostgreSQL 16)

* Persistent volume enabled
* Automatically initialized

---

## ⚙️ Environment Variables

Create `.env` file:

```env id="d8k2qp"
DEBUG=1
SECRET_KEY=your-secret-key

POSTGRES_DB=taskhub
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 📄 Docker Compose Overview

```yaml id="m2v9qp"
services:
  web:
    build: .
    command: gunicorn taskhub.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env

  db:
    image: postgres:16
    environment:
      POSTGRES_DB: taskhub
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

# 🔐 Authentication Header

```http id="v4x9ld"
Authorization: Token your_token_here
```

---

# 📌 Project Structure

```text id="b8m1qp"
Task_Management_API/

├── accounts/
├── Tasks/
├── project/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# 🔐 Security

* Token Authentication
* Role-Based Access Control
* User-Isolated Data Access
* Protected API Endpoints

---

# 🚀 Future Improvements

* JWT Authentication
* Email Notifications
* Task Reminders
* Full-Text Search
* Team Collaboration
* File Attachments
* Swagger / OpenAPI Documentation
* CI/CD with GitHub Actions

---

# 👨‍💻 Author

**Otieno Backend**

GitHub: [https://github.com/otieno-backend](https://github.com/otieno-backend)

---

# 📜 License

MIT License
