from django.urls import path
from .views import RegisterView, LoginView
from .views import (
    TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView, TaskListView
)
urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/update/<int:pk>', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/delete/<int:pk>', TaskDeleteView.as_view(), name='task-delete'),
]

