from rest_framework import generics, filters  
from rest_framework.permissions import IsAuthenticated, AllowAny  
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.response import Response  
from rest_framework import status  
from django.contrib.auth import get_user_model  
from .serializers import UserSerializer, LoginSerializer, TaskSerializer 
from .models import Task  
from .permissions import IsOwner  
from .models import Category  # Import Category model
from .serializers import CategorySerializer
from django.utils import timezone  # For checking due dates

User = get_user_model()  

#  User Management Views

# Register a New User (CREATE)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()  
    serializer_class = UserSerializer  
    permission_classes = [AllowAny] 

    # What happens when a user is created
    def perform_create(self, serializer):
        serializer.save()  # Save the new user

# Login View (Get Tokens)
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    # Handle POST request (when user sends email/password)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)  
        user = serializer.validated_data['user'] 
        refresh = RefreshToken.for_user(user)  
        return Response({
            'refresh': str(refresh),  
            'access': str(refresh.access_token), 
        }, status=status.HTTP_200_OK)  

# Task Management Views

# Create a Task (CREATE)
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated]  

    # When creating, link task to the logged-in user
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Save with current user

# View a Single Task (READ)
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()  # All tasks (filtered below)
    serializer_class = TaskSerializer  # Show task as JSON
    permission_classes = [IsAuthenticated, IsOwner]  # Must be logged in and own the task

    # Only show tasks belonging to the logged-in user
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

# Update a Task (UPDATE)
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated, IsOwner]

    # Only allow updating user’s own tasks
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    # Handle marking task as complete/incomplete
    def perform_update(self, serializer):
        from django.utils import timezone
        if serializer.validated_data.get('is_completed', False):
            serializer.save(completed_at=timezone.now())
        elif serializer.instance.is_completed:
            serializer.save(completed_at=None)
        else:
            serializer.save()  

# Delete a Task (DELETE)
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer  
    permission_classes = [IsAuthenticated, IsOwner] 

    # Only delete user’s own tasks
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

# List All Tasks with Filters and Sorting (READ)
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer 
    permission_classes = [IsAuthenticated]  
    filter_backends = [filters.OrderingFilter]  
    ordering_fields = ['due_date', 'priority']  

    # Filter tasks for the logged-in user with options
    def get_queryset(self):
        user = self.request.user  
        queryset = Task.objects.filter(created_by=user)  

        # Filter by completion status (true/false)
        is_completed = self.request.query_params.get('is_completed', None)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed.lower() == 'true')

        # Filter by priority (Low, Medium, High)
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)

        # Filter by category (by category ID now)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)

        return queryset  # Return the filtered list

# Category Views (Global)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer 
    permission_classes = [IsAuthenticated] 

    # When creating, no need for created_by (global)
    def perform_create(self, serializer):
        serializer.save()

# View/Update/Delete a Category
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all() 
    serializer_class = CategorySerializer 
    permission_classes = [IsAuthenticated] 


# Notification View (List Upcoming Tasks)
class NotificationView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user  # Current user
        now = timezone.now()  # Current time
        # Get tasks due soon (e.g., within 1 hour) that aren’t completed
        return Task.objects.filter(
            created_by=user,
            is_completed=False,
            due_date__gte=now,  # Due date is in the future
            due_date__lte=now + timezone.timedelta(hours=1)  # Within 1 hour
        )
