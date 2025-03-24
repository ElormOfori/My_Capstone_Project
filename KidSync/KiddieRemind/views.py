from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

User = get_user_model()

# Create your views here.
# Register a new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Login view
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# Create a Task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)  # Link task to logged-in user
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update a Task
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, id):
    try:
        task = Task.objects.get(id=id, created_by=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Delete a Task
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id, created_by=request.user)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# List Tasks
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    tasks = Task.objects.filter(created_by=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)






# List Tasks with Filtering, Sorting, and Searching
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    tasks = Task.objects.filter(created_by=request.user)

    # Filter by Category
    category = request.GET.get('category')
    if category:
        tasks = tasks.filter(category=category)

    # Search by Title
    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(Q(title__icontains=search))

    # Sort by Due Date
    sort_by = request.GET.get('sort_by', 'due_date')
    tasks = tasks.order_by(sort_by)

    # Paginate Results
    paginator = PageNumberPagination()
    paginator.page_size = 5
    result_page = paginator.paginate_queryset(tasks, request)
    serializer = TaskSerializer(result_page, many=True)
    
    return paginator.get_paginated_response(serializer.data)
