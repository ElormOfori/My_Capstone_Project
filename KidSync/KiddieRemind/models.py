from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Custom User Manager to helps create users
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):  # Make sure email is provided
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email) # Normalize email (e.g., make it lowercase)
        user = self.model(email=email, username=username, **extra_fields) # Create user with email, username, and any extra fields (like is_staff)
        user.set_password(password) # Set the password securely
        user.save(using=self._db)   # Save to database
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)  # Set extra fields for superusers (admin rights)
        return self.create_user(email, username, password, **extra_fields)  # Use create_user to make the superuser

# Custom User Model
class User(AbstractUser):
    email = models.EmailField(unique=True)  # Unique email for each user

    # Avoid conflicts with Django’s built-in User model
    groups = models.ManyToManyField("auth.Group", related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField("auth.Permission", related_name="custom_user_permissions", blank=True)

    objects = CustomUserManager()  # Use our custom manager
    USERNAME_FIELD = "email"       # Login with email instead of username
    REQUIRED_FIELDS = ["username"] # Username is still required

    def __str__(self):
        return self.email 

# Category Model (Global)
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.name  

# Priority Choices (for tasks)
PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

# Task Model
class Task(models.Model):
    title = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True) 
    due_date = models.DateTimeField() 
    is_completed = models.BooleanField(default=False)  
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Medium') 
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="tasks")  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks") 
    created_at = models.DateTimeField(auto_now_add=True)  
    completed_at = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return self.title
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")  # Who gets it
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notifications")  # Which task
    message = models.CharField(max_length=255)  # e.g., "Pack Lunch is due soon!"
    sent_at = models.DateTimeField(null=True, blank=True)  # When it was sent
    is_sent = models.BooleanField(default=False)  # Has it been sent yet?

    def __str__(self):
        return f"{self.message} for {self.user.email}"