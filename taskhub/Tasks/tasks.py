from datetime import timedelta
import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone

from .models import Task

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def send_due_soon_reminders():
    """
    Send reminder emails for tasks due within the next hour.
    """

    now = timezone.now()
    upcoming = now + timedelta(hours=1)

    tasks = (
        Task.objects.select_related("user")
        .filter(
            status=Task.Status.PENDING,
            due_date__gte=now,
            due_date__lte=upcoming,
        )
    )

    sent = 0

    for task in tasks:
        if not task.user.email:
            continue

        try:
            send_mail(
                subject=f"Reminder: {task.title}",
                message=(
                    f"Hello {task.user.username},\n\n"
                    f"This is a reminder that your task "
                    f"'{task.title}' is due at "
                    f"{timezone.localtime(task.due_date):%Y-%m-%d %H:%M} UTC."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.user.email],
                fail_silently=False,
            )
            sent += 1

        except Exception as exc:
            logger.exception(
                "Failed to send reminder for Task %s: %s",
                task.id,
                exc,
            )

    return f"Reminder emails sent: {sent}"


@shared_task
def notify_overdue_tasks():
    """
    Notify users about overdue pending tasks.
    """

    overdue_tasks = (
        Task.objects.select_related("user")
        .filter(
            status=Task.Status.PENDING,
            due_date__lt=timezone.now(),
        )
    )

    sent = 0

    for task in overdue_tasks:

        if not task.user.email:
            continue

        try:
            send_mail(
                subject=f"Overdue Task: {task.title}",
                message=(
                    f"Hello {task.user.username},\n\n"
                    f"Your task '{task.title}' is overdue.\n\n"
                    f"It was due on "
                    f"{timezone.localtime(task.due_date):%Y-%m-%d %H:%M} UTC.\n\n"
                    "Please complete it as soon as possible."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[task.user.email],
                fail_silently=False,
            )
            sent += 1

        except Exception as exc:
            logger.exception(
                "Failed to send overdue notification for Task %s: %s",
                task.id,
                exc,
            )

    return f"Overdue notifications sent: {sent}"


@shared_task
def cleanup_completed_tasks():
    """
    Delete completed tasks older than 30 days.
    """

    cutoff = timezone.now() - timedelta(days=30)

    deleted_count, _ = Task.objects.filter(
        status=Task.Status.COMPLETED,
        completed_at__lt=cutoff,
    ).delete()

    logger.info("Deleted %s completed tasks.", deleted_count)

    return f"Deleted {deleted_count} completed tasks."


@shared_task
def send_weekly_reports():
    """
    Email every user a summary of their tasks.
    """

    users = User.objects.filter(email__isnull=False).exclude(email="")

    emails_sent = 0

    for user in users:

        completed = Task.objects.filter(
            user=user,
            status=Task.Status.COMPLETED,
        ).count()

        pending = Task.objects.filter(
            user=user,
            status=Task.Status.PENDING,
        ).count()

        total = completed + pending

        try:
            send_mail(
                subject="Weekly Task Report",
                message=(
                    f"Hello {user.username},\n\n"
                    "Here is your weekly task summary.\n\n"
                    f"Total Tasks: {total}\n"
                    f"Completed: {completed}\n"
                    f"Pending: {pending}\n\n"
                    "Keep up the good work!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            emails_sent += 1

        except Exception as exc:
            logger.exception(
                "Failed to send weekly report to %s: %s",
                user.username,
                exc,
            )

    return f"Weekly reports sent: {emails_sent}"

