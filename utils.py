import os

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from dotenv import load_dotenv

load_dotenv()
load_dotenv(override=True)


def send_100views_notification(article):
    subject = f'Статья "{article.name}" достигла 100 просмотров!'

    article_url = reverse("blogs:blog_detail", kwargs={"pk": article.id})
    full_url = f"{settings.BASE_URL}{article_url}"

    message = (
        f"Поздравляем!\n\n"
        f'Статья "{article.name}" набрала 100 просмотров.\n'
        f"Ссылка: {full_url}\n\n"
        f"Время: {article.create_at}"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [os.getenv("EMAIL_HOST_USER")]  # Ваш email

    send_mail(subject, message, from_email, recipient_list)
