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
        queryset=Category.objects.all()
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    recurrence = serializers.ChoiceField(
        choices=Task.Recurrence.choices
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

    def validate_due_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )
        return value

    # 🔥 SINGLE SOURCE OF TRUTH FOR RULES
    def update(self, instance, validated_data):

        if instance.status == Task.Status.COMPLETED:
            allowed = {"title"}

            forbidden = set(validated_data.keys()) - allowed

            if forbidden:
                raise serializers.ValidationError(
                    "Only title can be updated for completed tasks."
                )

        return super().update(instance, validated_data)