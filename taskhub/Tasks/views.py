from django.db import models
from rest_framework import viewsets, permissions, status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action

from datetime import timedelta

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .pagination import TaskPagination


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskPagination

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        # Filters
        status_filter = self.request.query_params.get("status")
        priority_filter = self.request.query_params.get("priority")
        due_date = self.request.query_params.get("due_date")
        category = self.request.query_params.get("category")

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)

        if due_date:
            queryset = queryset.filter(due_date__date=due_date)

        if category:
            queryset = queryset.filter(
                models.Q(category__id=category) |
                models.Q(category__name__iexact=category)
            )

        # Sorting
        ordering = self.request.query_params.get("ordering")
        if ordering in ["due_date", "-due_date", "priority", "-priority"]:
            queryset = queryset.order_by(ordering)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        if task.status == "COMPLETED":
            return Response(
                {"error": "Completed tasks cannot be edited."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()

        if task.status == "COMPLETED":
            return Response(
                {"error": "Completed tasks cannot be edited."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().partial_update(request, *args, **kwargs)

    # 🔁 Helper: calculate next due date
    def get_next_due_date(self, task):
        if not task.due_date:
            return None

        if task.recurrence == "DAILY":
            return task.due_date + timedelta(days=1)

        if task.recurrence == "WEEKLY":
            return task.due_date + timedelta(weeks=1)

        if task.recurrence == "MONTHLY":
            return task.due_date + timedelta(days=30)

        return None

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        task = self.get_object()

        task.status = "COMPLETED"
        task.completed_at = timezone.now()
        task.save()

        # 🔁 Auto-create next recurring task
        if task.recurrence != "NONE":
            Task.objects.create(
                user=task.user,
                title=task.title,
                description=task.description,
                priority=task.priority,
                status="PENDING",
                due_date=self.get_next_due_date(task),
                recurrence=task.recurrence,
                category=task.category,
            )

        return Response(self.get_serializer(task).data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        