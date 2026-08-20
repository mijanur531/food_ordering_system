from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_order_confirmation_email(order):
    subject = f"Your order #{order.id} is confirmed!"
    message = (
        f"Hi {order.user.username},\n\n"
        f"Thanks for your order of Rs. {order.total_amount} placed on "
        f"{order.created_at.strftime('%d %b %Y, %I:%M %p')}.\n"
        f"Status: {order.get_status_display()}\n"
        f"Delivery address: {order.delivery_address}\n\n"
        f"We'll notify you as it moves through preparation and delivery.\n"
        f"— Your Food App Team"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)


def send_order_status_email(order):
    subject = f"Order #{order.id} update: {order.get_status_display()}"
    message = (
        f"Hi {order.user.username}, your order #{order.id} is now "
        f"'{order.get_status_display()}'."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email], fail_silently=True)


def send_contact_ack_email(contact_message):
    subject = "We received your message"
    message = (
        f"Hi {contact_message.name},\n\n"
        f"Thanks for reaching out — our team will get back to you shortly.\n\n"
        f"Your message:\n{contact_message.message}"
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [contact_message.email], fail_silently=True)
