from django.urls import path
from .views import RegisterView, LoginView
from .views import create_task, update_task, delete_task, list_tasks

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('tasks/create', create_task, name='create-task'),
    path('tasks/update/<int:id>', update_task, name='update-task'),
    path('tasks/delete/<int:id>', delete_task, name='delete-task'),
    path('tasks/list', list_tasks, name='list-tasks'),
]


