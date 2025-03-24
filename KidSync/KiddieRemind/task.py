from celery import shared_task
from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Task

@shared_task
def send_task_reminders():
    tasks = Task.objects.filter(due_date__lte=now(), is_completed=False)
    for task in tasks:
        send_mail(
            subject=f"Task Reminder: {task.title}",
            message=f"Reminder! Your task '{task.title}' is due soon.",
            from_email="no-reply@kiddieremind.com",
            recipient_list=[task.created_by.email],
        )
