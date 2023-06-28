from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_notification(subject, recipient_list, template_name, context):
    # Render email template
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)

    # Send email
    send_mail(subject, plain_message, None, recipient_list, html_message=html_message)
