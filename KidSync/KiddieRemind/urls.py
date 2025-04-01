from django.urls import path
from .views import (
    RegisterView, LoginView, TaskCreateView, TaskDetailView,
    TaskUpdateView, TaskDeleteView, TaskListView,
    CategoryListCreateView, CategoryDetailView, NotificationView
)

urlpatterns = [
    # User Management
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Task Management
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    # Category Management
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    # Notification Management
    path('notifications/', NotificationView.as_view(), name='notifications'),
]