import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from cell_rental_service.settings import SENDER_EMAIL
from order.models import Order

from celery import shared_task


@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Order #{order.id} confirmation"
    html_message = render_to_string(
        "../templates/order/order_email.html",
        {"order": order},
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=SENDER_EMAIL,
        recipient_list=[order.user_email],
        html_message=html_message,
    )


@shared_task
def send_email_reminders_about_lease_ending():
    now = datetime.datetime.now()
    reminder_time = now + datetime.timedelta(minutes=30)
    orders_to_remind = Order.objects.filter(
        end_timestamp__lt=reminder_time.timestamp(),
        reminded=False,
    )

    for order in orders_to_remind:
        send_email_reminder(order)


def send_email_reminder(order):
    subject = f"Order #{order.id} - Lease Ending Reminder"
    html_message = render_to_string(
        "../templates/order/order_email_reminder.html",
        {"order": order},
    )
    plain_message = strip_tags(html_message)
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=SENDER_EMAIL,
        recipient_list=[order.user_email],
        html_message=html_message,
    )
    order.reminded = True
    order.save()
