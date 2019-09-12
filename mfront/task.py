from celery import task
from django.core.mail import EmailMessage
import time
from meiduo import settings


@task
def send_email(email,token):
    title = '欢迎注册本网站'
    email_url = "点击此链接<a href='http://localhost:8000/valid_email?code="+token+"'>点此</a>链接进行用户激活"
    set_yin = settings.DEFAULT_FROM_EMAIL
    return 'ok'










