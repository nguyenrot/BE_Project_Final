from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class SendMail:
    @staticmethod
    def send_html_email(mail_data):
        subject, from_email, to = (
            mail_data.get("subject"),
            settings.EMAIL_HOST_USER,
            mail_data.get("to"),
        )

        html_content = render_to_string(
            mail_data.get("template"), mail_data.get("context")
        )
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, 'Dịch vụ công Epoch-making  <noreply@epoch-making.xyz>', to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
