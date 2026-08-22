from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
)
def send_email(subject, body, from_email, recipient_list, html_message=None):
    message = EmailMultiAlternatives(subject, body, from_email, recipient_list)
    if html_message:
        message.attach_alternative(html_message, 'text/html')
    message.send()
