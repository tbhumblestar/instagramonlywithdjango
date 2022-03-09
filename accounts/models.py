from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string


#class User(models.Model):
#이런식으로 user모델을 만들어줘도 되지만, 이렇게 하면 user모델이 활성된 user모델을 참조하는거라 에러가 날 수 있음
class User(AbstractUser):
  website_url = models.URLField(blank=True)
  bio = models.TextField(blank=True)

  def send_welcome_email(self):
    
    subject = render_to_string("accounts/welcome_email_subject.txt",{"user":self})
    content = render_to_string("accounts/welcome_email_content.txt",{"user":self})
    #두번쨰 인자의 값들을 넘겨준 값을 반영한, 첫번쨰 인자의 경로에 있는 파일의 내용을 str로 반환

    sender_email = settings.WELCOME_EMAIL_SENDER
    send_mail(subject,content,sender_email,[self.email],fail_silently=False)