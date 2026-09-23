import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from .models import Task


@pytest.mark.django_db
class TestTaskStatusWorkflow:

    def setup_method(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test task description",
            status=Task.Status.PENDING,
            priority=Task.Priority.MEDIUM,
        )

    def test_task_starts_as_pending(self):
        assert self.task.status == Task.Status.PENDING
        assert self.task.completed_at is None

    def test_task_can_be_changed_to_in_progress(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": Task.Status.IN_PROGRESS},
            format="json",
        )

        assert response.status_code == 200

        self.task.refresh_from_db()

        assert self.task.status == Task.Status.IN_PROGRESS
        assert self.task.completed_at is None

    def test_completing_task_sets_completed_at(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": Task.Status.COMPLETED},
            format="json",
        )

        assert response.status_code == 200

        self.task.refresh_from_db()

        assert self.task.status == Task.Status.COMPLETED
        assert self.task.completed_at is not None

    def test_completed_task_can_return_to_in_progress(self):
        self.task.status = Task.Status.COMPLETED
        self.task.completed_at = timezone.now()
        self.task.save()

        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": Task.Status.IN_PROGRESS},
            format="json",
        )

        assert response.status_code == 200

        self.task.refresh_from_db()

        assert self.task.status == Task.Status.IN_PROGRESS
        assert self.task.completed_at is None

    def test_task_can_be_cancelled(self):
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"status": Task.Status.CANCELLED},
            format="json",
        )

        assert response.status_code == 200

        self.task.refresh_from_db()

        assert self.task.status == Task.Status.CANCELLED
        assert self.task.completed_at is None
