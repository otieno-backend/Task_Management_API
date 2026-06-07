from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Task, Category

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="pass12345"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="pass12345"
        )

        self.category1 = Category.objects.create(user=self.user1, name="Work")
        self.category2 = Category.objects.create(user=self.user2, name="Home")

        self.task1 = Task.objects.create(
            user=self.user1,
            title="Task 1",
            status=Task.Status.PENDING,
            priority=Task.Priority.HIGH,
            due_date=timezone.now() + timedelta(days=1),
            category=self.category1,
            recurrence=Task.Recurrence.DAILY,
        )

        self.task2 = Task.objects.create(
            user=self.user1,
            title="Task 2",
            status=Task.Status.PENDING,
            priority=Task.Priority.LOW,
            due_date=timezone.now() + timedelta(days=2),
            category=self.category1,
            recurrence=Task.Recurrence.NONE,
        )

        self.task3 = Task.objects.create(
            user=self.user2,
            title="Task 3",
            status=Task.Status.PENDING,
            priority=Task.Priority.MEDIUM,
            due_date=timezone.now() + timedelta(days=3),
            category=self.category2,
            recurrence=Task.Recurrence.NONE,
        )


class TaskViewSetTests(BaseAPITest):

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_task_list_only_returns_user_tasks(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/tasks/")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(t["title"] != "Task 3" for t in res.data["results"]))

    def test_filter_by_status(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/tasks/?status=PENDING")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(t["status"] == "PENDING" for t in res.data["results"]))

    def test_filter_by_priority(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/tasks/?priority=HIGH")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(t["priority"] == "HIGH" for t in res.data["results"]))

    def test_filter_by_category_id(self):
        self.authenticate(self.user1)
        res = self.client.get(f"/api/tasks/?category={self.category1.id}")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(t["category"]["id"] == self.category1.id for t in res.data["results"]))

    def test_filter_by_category_name(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/tasks/?category=Work")

        self.assertEqual(res.status_code, 200)
        self.assertTrue(all(t["category"]["name"] == "Work" for t in res.data["results"]))

    def test_ordering(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/tasks/?ordering=-priority")

        self.assertEqual(res.status_code, 200)
        priorities = [t["priority"] for t in res.data["results"]]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_create_task_assigns_user(self):
        self.authenticate(self.user1)

        payload = {
            "title": "New Task",
            "priority": "HIGH",
            "status": "PENDING",
            "recurrence": "NONE",
        }

        res = self.client.post("/api/tasks/", payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["user"], self.user1.username)

    def test_complete_task_marks_completed(self):
        self.authenticate(self.user1)

        url = f"/api/tasks/{self.task1.id}/complete/"
        res = self.client.patch(url)

        self.assertEqual(res.status_code, 200)

        self.task1.refresh_from_db()
        self.assertEqual(self.task1.status, Task.Status.COMPLETED)
        self.assertIsNotNone(self.task1.completed_at)

    def test_complete_task_creates_next_recurrence(self):
        self.authenticate(self.user1)

        url = f"/api/tasks/{self.task1.id}/complete/"
        self.client.patch(url)

        recurring_task_exists = Task.objects.filter(
            user=self.user1,
            title=self.task1.title,
            status=Task.Status.PENDING
        ).exclude(id=self.task1.id).exists()

        self.assertTrue(recurring_task_exists)

    def test_complete_already_completed_task_fails(self):
        self.authenticate(self.user1)

        self.task1.status = Task.Status.COMPLETED
        self.task1.save()

        url = f"/api/tasks/{self.task1.id}/complete/"
        res = self.client.patch(url)

        self.assertEqual(res.status_code, 400)
        self.assertIn("error", res.data)


class CategoryViewSetTests(BaseAPITest):

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_user_sees_only_their_categories(self):
        self.authenticate(self.user1)
        res = self.client.get("/api/categories/")

        self.assertEqual(res.status_code, 200)
        names = [c["name"] for c in res.data]

        self.assertIn("Work", names)
        self.assertNotIn("Home", names)

    def test_create_category_assigns_user(self):
        self.authenticate(self.user1)

        res = self.client.post("/api/categories/", {"name": "Fitness"})

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Category.objects.filter(user=self.user1, name="Fitness").count(), 1)
        