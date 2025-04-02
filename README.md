


KiddieRemind Backend (KidSync)

Project Overview
Task Reminder with Notification Web App – A web-based task reminder app that helps parents Especially working mothers schedule and receive reminders for their kids' daily or weekly activities. The app will send notifications to ensure tasks are completed on time.
The KiddieRemind backend is built using Django and Django REST Framework (DRF) to provide authentication and user management for the KiddieRemind platform. 

Tech Stack
Django – Python web framework for building the backend.
Django REST Framework (DRF) – For API development.
djangorestframework-simplejwt – For JWT authentication.

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
pip install django djangorestframework djangorestframework-simplejwt

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





WEEK 4

KiddieRemind Backend (KidSync)
Project Overview
The KiddieRemind backend, built with Django and Django REST Framework (DRF), provides task management functionality for the KiddieRemind platform. The KidSync app handles user authentication, task creation, task reminders, and category-based organization.

Tech Stack
Django – Python web framework for backend development.
Django REST Framework (DRF) – For API creation and management.
djangorestframework-simplejwt – For authentication using JWT tokens.



Project Structure
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


2. Adding Filter, Sort & Search Functionality
Objective: Improve usability by allowing users to filter, search, and sort tasks.

Steps Taken:
Updated views to support search and filtering (KidSync/views.py):

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

WHY?
Enhances user efficiency in managing tasks.
Improves UX by allowing easy access to relevant tasks.
Migrations & Testing
After making these changes, I applied migrations and tested API endpoints:


python manage.py makemigrations KidSync
python manage.py migrate
python manage.py runserver



**TEST CASES**

**1. Testing the Register API (/api/register/)**
Valid Inputs
**_Test Case 1 (Successful Registration)_**
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123!"
}
Expected Response: 201 Created

Invalid Inputs
**_Test Case 2 (Missing Email)_**
{
  "username": "user2",
  "password": "SecurePass123!"
}
Expected Response: 400 Bad Request (Email is required)

**_Test Case 3 (Weak Password)_**
{
  "username": "user3",
  "email": "user3@example.com",
  "password": "123"
}
Expected Response: 400 Bad Request (Password too short)

**_Test Case 4 (Duplicate Username)_**
{
  "username": "newuser",
  "email": "another@example.com",
  "password": "SecurePass123!"
}
Expected Response: 400 Bad Request (Username already exists)

**_Test Case 5 (Invalid Email Format)_**
{
  "username": "user4",
  "email": "invalid-email",
  "password": "SecurePass123!"
}
Expected Response: 400 Bad Request (Invalid email format)



**2. Testing the Login API (/api/login/)**
Valid Login
**_Test Case 1 (Correct Credentials)_**
{
  "username": "newuser",
  "password": "SecurePass123!"
}
Expected Response: 200 OK + Token


Invalid Logins
**_Test Case 2 (Incorrect Password)_**
{
  "username": "newuser",
  "password": "WrongPass!"
}
Expected Response: 401 Unauthorized

**_Test Case 3 (Unregistered User)_**
{
  "username": "unknownuser",
  "password": "SomePass123!"
}
Expected Response: 401 Unauthorized

**_Test Case 4 (Missing Username)_**
{
  "password": "SecurePass123!"
}
 Expected Response: 400 Bad Request (Username required)

**_Test Case 5 (Missing Password)_**
{
  "username": "newuser"
}
Expected Response: 400 Bad Request (Password required)


**3. Testing the Category Creation API (/api/categories/)**
Valid Inputs
**_Test Case 1 (Successful Category Creation)_**
{
  "name": "Work"
}
Expected Response: 201 Created

Invalid Inputs
**_Test Case 2 (Missing Name)_**

{}
Expected Response: 400 Bad Request (Name is required)

**_Test Case 3 (Duplicate Name)_**
{
  "name": "Work"
}
Expected Response: 400 Bad Request (Category already exists)

**_Test Case 4 (Long Name)_**
{
  "name": "A very long category name that exceeds the character limit"
}
Expected Response: 400 Bad Request (Max length exceeded)

**_Test Case 5 (Invalid Data Type)_**
{
  "name": 12345
}
Expected Response: 400 Bad Request (Invalid type, should be string)

**4 . Testing the Task Creation API (/api/tasks/)**
Valid Inputs
**_Test Case 1 (Successful Task Creation)_**
{
  "title": "Complete Homework",
  "description": "Finish math and science assignments",
  "due_date": "2024-04-10",
  "priority": "High",
  "status": "Pending",
  "category": 1
}
Expected Response: 201 Created

Invalid Inputs
**_Test Case 2 (Missing Title)_**
{
  "description": "A task with no title",
  "due_date": "2024-04-10",
  "priority": "Medium",
  "status": "Pending",
  "category": 1
}
Expected Response: 400 Bad Request (Title is required)

**_Test Case 3 (Invalid Due Date - Past Date)_**
{
  "title": "Past Due Task",
  "description": "This task has an invalid due date",
  "due_date": "2023-01-01",
  "priority": "High",
  "status": "Pending",
  "category": 1
}
Expected Response: 400 Bad Request (Due date must be in the future)

**_Test Case 4 (Invalid Priority Value)_**
{
  "title": "Invalid Priority Task",
  "description": "This task has an invalid priority",
  "due_date": "2024-04-10T5:00:00Z",
  "priority": "Extreme",
  "status": "Pending",
  "category": 1
}
Expected Response: 400 Bad Request (Priority must be 'Low', 'Medium', or 'High')

**_Test Case 5 (Invalid Status Value)_**
{
  "title": "Invalid Status Task",
  "description": "This task has an invalid status",
  "due_date": "2024-04-10",
  "priority": "Medium",
  "status": "In Progress",
  "category": 1
}
**Filtering, Searching and Sorting**
**_Task Filtering_**
Test Case (Filter tasks by status = "Pending")
GET /api/tasks/?status=Pending
Expected Response: 200 OK (Returns all tasks where status = Pending)

**_Task Searching_**
Test Case (Search for tasks with "homework" in title or description)
GET /api/tasks/?search=homework
Expected Response: 200 OK (Returns tasks containing "homework" in title or description)

**_Task Ordering_**
Test Case (Order tasks by due date - Ascending)
GET /api/tasks/?ordering=due_date
Expected Response: 200 OK (Returns tasks sorted by due_date in ascending order)

**_Category Filtering_**
Test Case (Filter categories by name = "School")
GET /api/categories/?name=School
Expected Response: 200 OK (Returns all categories named "School")

**_Category Searching_**
Test Case (Search for categories containing "Work")
GET /api/categories/?search=Work
Expected Response: 200 OK (Returns categories containing "Work")

**_Category Ordering_**
Test Case (Order categories alphabetically by name)
GET /api/categories/?ordering=name
Expected Response: 200 OK (Returns categories sorted alphabetically)