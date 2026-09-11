# Task Management API

A RESTful Task Management API built with Django REST Framework. The project provides secure task management, user authentication, role-based permissions, filtering, pagination, and support for recurring tasks using background jobs.

## 🌐 Live Demo

Live API: https://task-management-api-wpw5.onrender.com/api/

The API is deployed on Render and available for testing.

## 🚀 Features

User registration and authentication

Create, update, view, and delete tasks

Task status and priority management

Task categories

Filtering, sorting, and pagination

Role-based permissions

Recurring tasks

Background task processing with Celery

Redis integration

PostgreSQL database support

Docker support

Production deployment with Gunicorn

## 🛠️ Tech Stack

Python

Django

Django REST Framework

PostgreSQL

Redis

Celery

Docker

Gunicorn

Render

## 🏗️ Project Structure

Task_Management_API/

├── accounts/       # User authentication and permissions

├── Tasks/          # Task management functionality

├── taskhub/        # Django project configuration

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

└── manage.py

## ⚙️ Getting Started
 Clone the repository

 git clone https://github.com/otieno-backend/Task_Management_API.git

 cd Task_Management_API

### Create a virtual environment
python -m venv venv


Activate it:

### Linux/macOS

source venv/bin/activate


### Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Start the server

python manage.py runserver


The API will be available at:

http://localhost:8000/

### 🔐 Authentication

The API uses token-based authentication.

After logging in, include the token in requests:

Authorization: Token YOUR_TOKEN

### 🐳 Docker

The project can also be run using Docker:

docker compose up --build

### 🌐 Live API

The API is deployed on Render:

https://task-management-api-wpw5.onrender.com/api/

### 📌 What I Built

This project demonstrates my ability to:

 Design and build RESTful APIs
 
 Implement authentication and authorization
 
 Work with relational databases
 
 Build asynchronous background processes
 
 Containerize applications with Docker
 
 Deploy backend applications
 
 Structure a maintainable Django project

### 👨‍💻 Author

Otieno Backend

GitHub:

https://github.com/otieno-backend/Task_Management_API

⭐ If you find this project useful, feel free to star the repository.