import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery import shared_task

# Настройки SMTP сервера
smtp_server = 'smtp.yandex.ru'  # Замените на ваш SMTP сервер
smtp_port = 465  # Замените на ваш SMTP порт
smtp_user = os.getenv('EMAIL_NAME')  # Ваш email
smtp_password = os.getenv('EMAIL_PASSWORD')  # Ваш пароль


@shared_task
def send_email(subject, body, to_email):
    # Создание сообщения
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(smtp_server)
    server.set_debuglevel(1)
    server.ehlo(smtp_user)
    server.login(smtp_user, smtp_password)
    server.auth_plain()
    # Отправка письма
    server.sendmail(smtp_user, to_email, msg.as_string())
