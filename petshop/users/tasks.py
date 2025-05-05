from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .services import send_sms


@shared_task
def send_email_task(*, email: str, content: str, subject: str):
    send_mail(
        subject=subject,
        message=content,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


@shared_task
def send_sms_task(phone_number: str, content: str):
    send_sms(phone_number=phone_number, content=content)
