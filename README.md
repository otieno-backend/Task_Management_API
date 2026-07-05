# 🚀 Task Management API

A production-ready **Task Management REST API** built with **Django** and **Django REST Framework**.
It enables secure, scalable task management with authentication, role-based access control, recurring task automation, and background processing using Celery.

---

## 🌐 Live Demo

* 🔗 API: [Task Management API](https://task-management-api-wpw5.onrender.com/?utm_source=chatgpt.com)
* 💻 Repository: [GitHub Repository](https://github.com/otieno-backend/Task_Management_API?utm_source=chatgpt.com) (hosted on GitHub)

---

## ✨ Key Features

### 🔐 Authentication & Security

* Token-based authentication (DRF Token Auth)
* User registration & login
* Protected endpoints
* User data isolation
* Production-ready security settings (HSTS, secure cookies, clickjacking protection)

---

### 👥 Role-Based Access Control

* Admin vs regular user permissions
* Users can only access their own tasks
* Secure object-level access control

---

### ✅ Task Management

Users can:

* Create, update, delete tasks
* Mark tasks as completed
* Assign priorities (Low / Medium / High)
* Organize tasks using categories
* Set due dates
* Track task status

---

### 🔁 Recurring Tasks (Celery-powered)

Automated task regeneration using **Celery + Redis + django-celery-beat**:

* Daily tasks
* Weekly tasks
* Monthly tasks
* Automatic next-task generation after completion

---

### 🔎 Filtering, Sorting & Pagination

* Filter by status, priority, category, due date
* Sort by due date or priority
* Paginated API responses for scalability

---

## 🧱 Tech Stack

| Layer        | Technology               |
| ------------ | ------------------------ |
| Backend      | Django 4.2               |
| API          | Django REST Framework    |
| Database     | PostgreSQL / SQLite      |
| Async Tasks  | Celery                   |
| Broker       | Redis                    |
| Scheduler    | django-celery-beat       |
| Auth         | DRF Token Authentication |
| Server       | Gunicorn                 |
| Static Files | WhiteNoise               |
| Deployment   | Docker, Render           |

---

## 🏗️ System Architecture

```
Client → Django REST API → PostgreSQL
                     ↓
                Redis Broker
                     ↓
              Celery Workers
                     ↓
        Recurring Task Scheduler
```

---

## 📦 Project Structure

```
Task_Management_API/
│
├── accounts/          # Authentication & permissions
├── Tasks/             # Core task management logic
├── taskhub/           # Project configuration
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── manage.py
```

---

## 🔗 API Base URL

### Local

```
http://localhost:8000/api/
```

### Production

```
https://task-management-api-wpw5.onrender.com/api/
```

---

## 🔑 Authentication Flow

### 1. Register User

```http
POST /api/register/
```

### 2. Login

```http
POST /api/login/
```

Response:

```json
{
  "token": "your_auth_token"
}
```

### 3. Use Token

```http
Authorization: Token your_auth_token
```

---

## 📌 Core API Endpoints

| Method | Endpoint       | Description       |
| ------ | -------------- | ----------------- |
| POST   | `/register/`   | Create user       |
| POST   | `/login/`      | Authenticate user |
| GET    | `/tasks/`      | List tasks        |
| POST   | `/tasks/`      | Create task       |
| GET    | `/tasks/{id}/` | Retrieve task     |
| PUT    | `/tasks/{id}/` | Update task       |
| DELETE | `/tasks/{id}/` | Delete task       |
| GET    | `/categories/` | List categories   |

---

## 📤 Example Request

```http
POST /api/tasks/
Authorization: Token your_token
```

```json
{
  "title": "Complete Django Project",
  "description": "Finish Task Management API",
  "priority": "High",
  "status": "Pending",
  "due_date": "2026-07-15"
}
```

---

## 🔍 Filtering Examples

```http
GET /api/tasks/?status=Pending
GET /api/tasks/?priority=High
GET /api/tasks/?ordering=due_date
GET /api/tasks/?page=2
```

---

## 🐳 Docker Setup

### Clone Repository

```bash
git clone https://github.com/otieno-backend/Task_Management_API.git
cd Task_Management_API
```

### Run Containers

```bash
docker compose up --build
```

### Run in Background

```bash
docker compose up -d
```

### Migrate Database

```bash
docker compose exec web python manage.py migrate
```

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```env
DEBUG=True
SECRET_KEY=your-secret-key

POSTGRES_DB=taskhub
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## 🔄 Background Jobs

Powered by **Celery + Redis**:

* Recurring task generation
* Scheduled task execution
* Periodic job scheduling via django-celery-beat

---

## 🧪 Testing

Run automated tests:

```bash
pytest
```

Optional coverage:

```bash
coverage run -m pytest
coverage report
```

---

## 🧠 Design Decisions

* **Token Auth** → simple, stateless authentication for API-first design
* **Celery** → reliable background task execution for recurring tasks
* **PostgreSQL** → production-grade relational database
* **Docker** → consistent development and deployment environment

---

## 📈 Future Improvements

* JWT authentication upgrade
* Email & push notifications for due tasks
* WebSocket real-time updates
* Advanced analytics dashboard
* Rate limiting & API throttling
* Task sharing between users

---

## 🚀 Deployment

Production stack:

* Render (hosting)
* Gunicorn (WSGI server)
* WhiteNoise (static files)
* PostgreSQL (database)
* Redis (message broker)
* Docker (containerization)

---

## 👨‍💻 Author

**Otieno Backend**

* GitHub: [GitHub Profile](https://github.com/otieno-backend?utm_source=chatgpt.com)

