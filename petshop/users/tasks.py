from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email(*, email: str, content: str, subject: str):
    send_mail(
        subject=subject,
        message=content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
