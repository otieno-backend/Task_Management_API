from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Task
from .pagination import TaskPagination
from .serializers import CategorySerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskPagination

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_next_due_date(self, task):
        """Calculate the next due date for recurring tasks."""
        if not task.due_date or task.recurrence == Task.Recurrence.NONE:
            return None

        recurrence_map = {
            Task.Recurrence.DAILY: timedelta(days=1),
            Task.Recurrence.WEEKLY: timedelta(weeks=1),
        }

        if task.recurrence in recurrence_map:
            return task.due_date + recurrence_map[task.recurrence]

        if task.recurrence == Task.Recurrence.MONTHLY:
            return task.due_date + relativedelta(months=1)

        return None

    def create_recurring_task(self, task):
        """Create the next occurrence of a recurring task."""
        next_due_date = self.get_next_due_date(task)

        Task.objects.create(
            user=task.user,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=Task.Status.PENDING,
            due_date=next_due_date,
            recurrence=task.recurrence,
            category=task.category,
        )

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.Status.COMPLETED:
            return Response(
                {"detail": "Task is already completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.status = Task.Status.COMPLETED
        task.completed_at = timezone.now()
        task.save(update_fields=["status", "completed_at"])

        if task.recurrence != Task.Recurrence.NONE:
            self.create_recurring_task(task)

        return Response(
            self.get_serializer(task).data,
            status=status.HTTP_200_OK,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        
