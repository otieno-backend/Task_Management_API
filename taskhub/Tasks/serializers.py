from rest_framework import serializers
from .models import Task, Category
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    # full nested category object
    category = CategorySerializer(read_only=True)

    # category id for write operations
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True
    )

    # category name (read-only)
    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    # 🔁 NEW: recurrence field
    recurrence = serializers.ChoiceField(
        choices=Task.Recurrence.choices,
        default=Task.Recurrence.NONE
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "status",

            # category
            "category",
            "category_id",
            "category_name",

            # 🔁 recurrence
            "recurrence",

            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )
        return value
