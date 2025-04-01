from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Task, Category, Notification
from django.utils import timezone

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Hide password in output

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Create new user
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid login credentials")
        return {'user': user}

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']  # No created_by anymore
        read_only_fields = ['created_at']

# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Show category details
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )  # Pick category by ID

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'is_completed', 'priority', 'category', 'category_id', 'created_by', 'created_at', 'completed_at']
        read_only_fields = ['created_by', 'created_at', 'completed_at']

    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future!")
        return value

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'task', 'message', 'sent_at', 'is_sent']  # Include all fields
        read_only_fields = ['sent_at', 'is_sent']  # User can’t set these manually