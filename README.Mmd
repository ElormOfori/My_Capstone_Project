


KiddieRemind Backend (KidSync)

Project Overview
The KiddieRemind backend is built using Django and Django REST Framework (DRF) to provide authentication and user management for the KiddieRemind platform. The core functionality is implemented in the KidSync app, which handles user registration, login, and JWT-based authentication.

Tech Stack
Django – Python web framework for building the backend.
Django REST Framework (DRF) – For API development.
djangorestframework-simplejwt – For JWT authentication.
django-cors-headers – For handling cross-origin requests.

Project Structure
My_Capstone_Project/
│── KiddieRemind/  # Django Project
│── KidSync/       # Django App for authentication
│── manage.py      # Django management script
│── README.md      # Documentation

Setup and Installation
1. Clone the Repository
git clone git clone https://github.com/ElormOfori/My_Capstone_Project.git
cd My_Capstone_Project


2. Install Dependencies
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt

4. Initialize Django Project
python3 -m django startproject KiddieRemind

5. Create Django App
python3 manage.py startapp KidSync

Configuration
Update settings.py
Add required apps:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'KidSync',
]

Enable CORS for frontend communication:
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

User Authentication
Custom User Model (KidSync/models.py)
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username

Set this model in settings.py:
AUTH_USER_MODEL = 'KidSync.User'

Migrations
python manage.py makemigrations KidSync
python manage.py migrate

API Endpoints
1. User Registration
Endpoint: POST /api/auth/register/
Request Body:
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

Response:
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
}

2. User Login
Endpoint: POST /api/auth/login/
Request Body:
{
    "username": "testuser",
    "password": "password123"
}

Response:
{
    "refresh": "jwt_refresh_token_here",
    "access": "jwt_access_token_here"
}

Running the Server
python manage.py runserver

Push Changes to GitHub
git add .
git commit -m "Added authentication system"
git push origin main


Next Steps
Set up Task Management
Implement task filtering, sorting, and permissions.
Add notifications system.
Optimize performance, security, and edge cases.
Final testing, documentation, and deployment.



WEEK 3 

KiddieRemind Backend (KidSync)
Project Overview
The KiddieRemind backend, built with Django and Django REST Framework (DRF), provides task management functionality for the KiddieRemind platform. The KidSync app handles user authentication, task creation, task reminders, and category-based organization.

Tech Stack
Django – Python web framework for backend development.
Django REST Framework (DRF) – For API creation and management.
Celery & Redis – For background task scheduling (email reminders).
djangorestframework-simplejwt – For authentication using JWT tokens.
django-cors-headers – For handling cross-origin requests.
Project Structure
bash
Copy
Edit
My_Capstone_Project/
│── KiddieRemind/  # Django Project
│── KidSync/       # Django App for authentication & task management
│── manage.py      # Django management script
│── README.md      # Documentation
Today's Implementations
1. Adding Task Categories
Objective: Categorize tasks into homework, chores, extracurricular activities, etc.

Steps Taken:

Updated the Task model (KidSync/models.py) to include a category field.
Modified serializers to handle categories.
Updated views to allow task categorization during creation and updates.
Code Changes:

python
Copy
Edit
class Task(models.Model):
    CATEGORY_CHOICES = [
        ('homework', 'Homework'),
        ('chores', 'Chores'),
        ('activity', 'Extracurricular'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    due_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
Why?

Helps users organize tasks efficiently.
Allows for future filtering and sorting based on task type.
2. Implementing Task Reminders via Email
Objective: Automatically remind users about upcoming tasks via email.

Steps Taken:

Installed Celery and Redis for background task processing:
bash
Copy
Edit
pip install celery redis django-celery-beat
Configured Celery in KiddieRemind/settings.py:
python
Copy
Edit
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
Created a Celery task (KidSync/tasks.py) to send email reminders.
python
Copy
Edit
from celery import shared_task
from django.core.mail import send_mail
from .models import Task
from datetime import datetime, timedelta

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(due_date__date=datetime.today().date())
    for task in tasks:
        send_mail(
            f"Reminder: {task.title}",
            f"Don't forget to complete your task: {task.title}",
            'noreply@kiddieremind.com',
            [task.user.email],
        )
Scheduled the task to run every day using Celery Beat.
Why?

Ensures users stay on top of their tasks.
Reduces missed deadlines and improves task completion.
3. Adding Filter, Sort & Search Functionality
Objective: Improve usability by allowing users to filter, search, and sort tasks.

Steps Taken:

Updated views to support search and filtering (KidSync/views.py):
python
Copy
Edit
from rest_framework import generics, filters
from .models import Task
from .serializers import TaskSerializer

class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['due_date']
Filter by Category:
Users can now retrieve tasks based on category (GET /tasks/list?category=homework).
Search by Title:
Users can search for specific tasks using keywords (GET /tasks/list?search=math).
Sort by Due Date:
Tasks can be sorted by deadline (GET /tasks/list?ordering=due_date).
Why?

Enhances user efficiency in managing tasks.
Improves UX by allowing easy access to relevant tasks.
Migrations & Testing
After making these changes, we applied migrations and tested API endpoints:

bash
Copy
Edit
python manage.py makemigrations KidSync
python manage.py migrate
python manage.py runserver
Testing Done:
Verified task categories in Postman.
Ensured email reminders were correctly scheduled and sent.
Checked filtering, searching, and sorting functionality.

