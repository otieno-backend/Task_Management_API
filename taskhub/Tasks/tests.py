from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task, Category

User = get_user_model()


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="Bra123#"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Work",
            user=self.user
        )

        self.task = Task.objects.create(
            user=self.user,
            title="Finish Project",
            description="DRF Project",
            priority=Task.Priority.HIGH,
            status=Task.Status.PENDING,
            recurrence=Task.Recurrence.NONE,
            category=self.category
        )

    def test_create_task(self):
        url = reverse("task-list")

        data = {
            "title": "New Task",
            "description": "Testing",
            "priority": "MEDIUM",
            "status": "PENDING",
            "recurrence": "NONE",
            "category": self.category.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 2)

    def test_get_tasks(self):
        url = reverse("task-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

    def test_filter_by_status(self):
        url = reverse("task-list")

        response = self.client.get(url, {"status": "PENDING"})

        self.assertEqual(response.status_code, 200)

        results = response.data["results"]
        self.assertTrue(all(task["status"] == "PENDING" for task in results))

    def test_update_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})

        response = self.client.patch(
            url,
            {"priority": "LOW"},
            format="json"
        )

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertEqual(self.task.priority, "LOW")

    def test_delete_task(self):
        url = reverse("task-detail", kwargs={"pk": self.task.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_completed_task_title_can_be_updated(self):
        self.task.status = Task.Status.COMPLETED
        self.task.save()

        url = reverse("task-detail", kwargs={"pk": self.task.id})

        response = self.client.patch(
            url,
            {"title": "Updated Title"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Title")

    def test_completed_task_priority_cannot_be_updated(self):
        self.task.status = Task.Status.COMPLETED
        self.task.save()

        url = reverse("task-detail", kwargs={"pk": self.task.id})

        response = self.client.patch(
            url,
            {"priority": "LOW"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_completed_task_status_cannot_be_changed(self):
        self.task.status = Task.Status.COMPLETED
        self.task.save()

        url = reverse("task-detail", kwargs={"pk": self.task.id})

        response = self.client.patch(
            url,
            {"status": "PENDING"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_task_endpoint(self):
        url = reverse("task-complete", kwargs={"pk": self.task.id})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.task.refresh_from_db()

        self.assertEqual(self.task.status, Task.Status.COMPLETED)
        self.assertIsNotNone(self.task.completed_at)


class CategoryAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="Bra123#"
        )

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name="Work",
            user=self.user
        )

    def test_create_category(self):
        url = reverse("category-list")

        response = self.client.post(url, {"name": "Personal"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_categories(self):
        url = reverse("category-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})

        response = self.client.patch(url, {"name": "Office"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Office")

    def test_delete_category(self):
        url = reverse("category-detail", kwargs={"pk": self.category.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Category.objects.filter(id=self.category.id).exists())
        