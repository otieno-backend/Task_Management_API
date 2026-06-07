from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from .pagination import TaskPagination


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = TaskPagination

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

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
            if category.isdigit():
                queryset = queryset.filter(category__id=int(category))
            else:
                queryset = queryset.filter(category__name__iexact=category)

        ALLOWED_ORDERING = {"due_date", "-due_date", "priority", "-priority"}

        ordering = self.request.query_params.get("ordering")

        if ordering in ALLOWED_ORDERING:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")  

        return queryset

    def get_serializer_context(self):
        return {"request": self.request}
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_next_due_date(self, task):
        
        if not task.due_date:
            return None
        
        if task.recurrence == Task.Recurrence.DAILY:
            return task.due_date + timedelta(days=1)

        if task.recurrence == Task.Recurrence.WEEKLY:
            return task.due_date + timedelta(weeks=1)

        if task.recurrence == Task.Recurrence.MONTHLY:
            return task.due_date + relativedelta(months=1)

        return None

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        task = self.get_object()

        if task.status == Task.Status.COMPLETED:
            return Response(
                {"error": "Task already completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        task.status = Task.Status.COMPLETED
        task.completed_at = timezone.now()
        task.save()

        next_due_date = self.get_next_due_date(task)

        if task.recurrence != Task.Recurrence.NONE and next_due_date:
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

        return Response(self.get_serializer(task).data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        