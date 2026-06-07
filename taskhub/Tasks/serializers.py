from rest_framework import serializers
from django.utils import timezone

from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
        queryset=Category.objects.all()  # FIX: prevents cross-user leakage
    )

    category_name = serializers.CharField(source="category.name", read_only=True)

    recurrence = serializers.ChoiceField(choices=Task.Recurrence.choices)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "user",
            "priority",
            "status",
            "category",
            "category_id",
            "category_name",
            "recurrence",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            self.fields["category_id"].queryset = Category.objects.filter(
                user=request.user
            )

    def validate(self, attrs):
        instance = getattr(self, "instance", None)

        if instance and instance.status == Task.Status.COMPLETED:
            allowed_fields = {"title"}

            for field in attrs:
                if field not in allowed_fields:
                    raise serializers.ValidationError({field: f"{field} cannot be updated for completed tasks."})
                
        return attrs
    